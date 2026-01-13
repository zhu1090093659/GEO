"""
Citation Module - Business Logic Service

Handles citation extraction, source tracking,
and website analysis using database storage.
"""
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any, Tuple
import re
import json
from urllib.parse import urlparse

from sqlalchemy import select, func, desc, and_
from sqlalchemy.ext.asyncio import AsyncSession

from .models import (
    Citation, CitationSource, WebsiteAnalysis,
    CitationType, SourceType, AnalysisStatus
)
from .schemas import (
    CitationDiscoveryResponse,
    CitationSourceItem,
    CitationItem,
    WebsiteAnalysisResponse,
    WebsiteRecommendation,
    CitationContextItem,
    AnalysisStatusResponse,
    CitationStatsResponse,
    ExtractCitationsResponse,
)

# Import tracking models for conversation lookup
from src.modules.tracking.models import Conversation, Message


# URL and domain extraction patterns
URL_PATTERN = re.compile(r'https?://[^\s<>"{}|\\^`\[\]]+')
DOMAIN_PATTERN = re.compile(
    r'(?:according to |source: |from |via |per |cited by )([a-zA-Z0-9][-a-zA-Z0-9]*(?:\.[a-zA-Z]{2,})+)',
    re.IGNORECASE
)
NAMED_SOURCE_PATTERN = re.compile(
    r'(?:according to |source: |from |via )([A-Z][a-zA-Z\s]+?)(?:,|\.|;|$)',
    re.MULTILINE
)


def normalize_domain(domain: str) -> str:
    """Normalize a domain for consistent matching."""
    domain = domain.lower().strip()
    if domain.startswith('www.'):
        domain = domain[4:]
    return domain


def extract_domain_from_url(url: str) -> Optional[str]:
    """Extract domain from URL."""
    try:
        parsed = urlparse(url)
        return normalize_domain(parsed.netloc) if parsed.netloc else None
    except Exception:
        return None


def classify_source_type(domain: str) -> SourceType:
    """Classify source type based on domain."""
    domain_lower = domain.lower()
    
    if domain_lower.endswith('.gov'):
        return SourceType.GOV
    elif domain_lower.endswith('.edu'):
        return SourceType.EDU
    elif any(news in domain_lower for news in [
        'nytimes', 'bbc', 'reuters', 'cnn', 'washingtonpost',
        'theguardian', 'forbes', 'bloomberg', 'wsj', 'news'
    ]):
        return SourceType.NEWS
    elif any(academic in domain_lower for academic in [
        'arxiv', 'scholar', 'pubmed', 'researchgate', 'jstor',
        'springer', 'wiley', 'nature.com', 'science.org'
    ]):
        return SourceType.ACADEMIC
    elif any(social in domain_lower for social in [
        'twitter', 'x.com', 'facebook', 'linkedin', 'reddit',
        'instagram', 'tiktok', 'youtube'
    ]):
        return SourceType.SOCIAL
    elif any(docs in domain_lower for docs in [
        'docs.', 'documentation', 'readme', 'github.io',
        'developer.', 'api.'
    ]):
        return SourceType.DOCS
    elif any(ecom in domain_lower for ecom in [
        'amazon', 'ebay', 'shopify', 'etsy', 'alibaba'
    ]):
        return SourceType.ECOMMERCE
    else:
        return SourceType.WEBSITE


def calculate_authority_score(domain: str, source_type: SourceType) -> float:
    """Calculate authority score for a domain."""
    base_scores = {
        SourceType.GOV: 90.0,
        SourceType.EDU: 85.0,
        SourceType.ACADEMIC: 85.0,
        SourceType.NEWS: 75.0,
        SourceType.DOCS: 70.0,
        SourceType.WEBSITE: 50.0,
        SourceType.SOCIAL: 40.0,
        SourceType.ECOMMERCE: 45.0,
        SourceType.UNKNOWN: 30.0,
    }
    
    score = base_scores.get(source_type, 50.0)
    
    # Bonus for well-known domains
    known_high_authority = [
        'wikipedia.org', 'github.com', 'stackoverflow.com',
        'medium.com', 'microsoft.com', 'google.com', 'apple.com'
    ]
    if any(known in domain.lower() for known in known_high_authority):
        score = min(100, score + 10)
    
    return score


class CitationService:
    """Service for citation discovery and website analysis."""
    
    # ========================================
    # Citation Extraction
    # ========================================
    
    async def extract_citations_from_text(
        self,
        db: AsyncSession,
        text: str,
        conversation_id: Optional[str] = None,
        message_id: Optional[int] = None,
    ) -> ExtractCitationsResponse:
        """
        Extract citations from AI response text.
        
        Args:
            db: Database session
            text: AI response text
            conversation_id: Associated conversation ID
            message_id: Associated message ID
            
        Returns:
            Extraction results with citations found
        """
        citations_created: List[Citation] = []
        sources_updated = 0
        
        # Extract URLs
        for match in URL_PATTERN.finditer(text):
            url = match.group()
            domain = extract_domain_from_url(url)
            if not domain:
                continue
            
            citation = Citation(
                conversation_id=conversation_id,
                message_id=message_id,
                source_url=url,
                source_domain=domain,
                citation_type=CitationType.URL.value,
                authority_score=0,  # Will be updated from source
                confidence=0.95,
                context=self._get_context(text, match.start(), match.end()),
                position=match.start(),
            )
            db.add(citation)
            citations_created.append(citation)
            
            # Update or create source
            await self._update_source(db, domain, CitationType.URL)
            sources_updated += 1
        
        # Extract domain references
        for match in DOMAIN_PATTERN.finditer(text):
            domain = normalize_domain(match.group(1))
            
            citation = Citation(
                conversation_id=conversation_id,
                message_id=message_id,
                source_domain=domain,
                citation_type=CitationType.DOMAIN.value,
                authority_score=0,
                confidence=0.85,
                context=self._get_context(text, match.start(), match.end()),
                position=match.start(),
            )
            db.add(citation)
            citations_created.append(citation)
            
            await self._update_source(db, domain, CitationType.DOMAIN)
            sources_updated += 1
        
        # Extract named sources
        for match in NAMED_SOURCE_PATTERN.finditer(text):
            source_name = match.group(1).strip()
            if len(source_name) < 3 or len(source_name) > 50:
                continue
            
            citation = Citation(
                conversation_id=conversation_id,
                message_id=message_id,
                source_name=source_name,
                citation_type=CitationType.NAMED.value,
                authority_score=50.0,
                confidence=0.7,
                context=self._get_context(text, match.start(), match.end()),
                position=match.start(),
            )
            db.add(citation)
            citations_created.append(citation)
        
        await db.commit()
        
        # Refresh citations to get IDs
        for citation in citations_created:
            await db.refresh(citation)
        
        return ExtractCitationsResponse(
            citations_found=len(citations_created),
            citations=[
                CitationItem(
                    id=c.id,
                    source_url=c.source_url,
                    source_domain=c.source_domain,
                    source_name=c.source_name,
                    citation_type=c.citation_type,
                    authority_score=c.authority_score,
                    confidence=c.confidence,
                    context=c.context,
                    created_at=c.created_at,
                )
                for c in citations_created
            ],
            sources_updated=sources_updated,
        )
    
    async def _update_source(
        self,
        db: AsyncSession,
        domain: str,
        citation_type: CitationType,
    ) -> CitationSource:
        """Update or create citation source record."""
        normalized = normalize_domain(domain)
        
        result = await db.execute(
            select(CitationSource).where(CitationSource.normalized_domain == normalized)
        )
        source = result.scalar_one_or_none()
        
        if source:
            source.citation_count += 1
            source.last_cited_at = datetime.utcnow()
        else:
            source_type = classify_source_type(domain)
            authority = calculate_authority_score(domain, source_type)
            
            source = CitationSource(
                domain=domain,
                normalized_domain=normalized,
                source_type=source_type.value,
                authority_score=authority,
                citation_count=1,
            )
            db.add(source)
        
        await db.flush()
        return source
    
    def _get_context(self, text: str, start: int, end: int, window: int = 100) -> str:
        """Get surrounding context for a citation."""
        ctx_start = max(0, start - window)
        ctx_end = min(len(text), end + window)
        return text[ctx_start:ctx_end].strip()
    
    # ========================================
    # Citation Discovery
    # ========================================
    
    async def discover_citations(
        self,
        db: AsyncSession,
        brand: Optional[str] = None,
        source_type: Optional[str] = None,
        limit: int = 50,
        days: int = 30,
    ) -> CitationDiscoveryResponse:
        """
        Discover citations from collected data.
        
        Args:
            db: Database session
            brand: Optional brand filter
            source_type: Optional source type filter
            limit: Maximum results
            days: Period in days
            
        Returns:
            Citation discovery results
        """
        start_date = datetime.utcnow() - timedelta(days=days)
        
        # Get total citations
        total_result = await db.execute(
            select(func.count(Citation.id))
            .where(Citation.created_at >= start_date)
        )
        total_citations = total_result.scalar() or 0
        
        # Get sources with counts
        source_query = (
            select(CitationSource)
            .where(CitationSource.is_active == True)
            .order_by(desc(CitationSource.citation_count))
            .limit(limit)
        )
        
        if source_type:
            source_query = source_query.where(CitationSource.source_type == source_type)
        
        sources_result = await db.execute(source_query)
        sources = sources_result.scalars().all()
        
        # Count by citation type
        type_result = await db.execute(
            select(Citation.citation_type, func.count(Citation.id))
            .where(Citation.created_at >= start_date)
            .group_by(Citation.citation_type)
        )
        by_type = {row[0]: row[1] for row in type_result.all()}
        
        # Count by source type
        source_type_result = await db.execute(
            select(CitationSource.source_type, func.sum(CitationSource.citation_count))
            .group_by(CitationSource.source_type)
        )
        by_source_type = {row[0]: int(row[1] or 0) for row in source_type_result.all()}
        
        return CitationDiscoveryResponse(
            total_citations=total_citations,
            total_sources=len(sources),
            sources=[
                CitationSourceItem(
                    id=s.id,
                    domain=s.domain,
                    display_name=s.display_name,
                    source_type=s.source_type,
                    authority_score=s.authority_score,
                    citation_count=s.citation_count,
                    avg_sentiment=s.avg_sentiment,
                    first_cited_at=s.first_cited_at,
                    last_cited_at=s.last_cited_at,
                    is_verified=s.is_verified,
                )
                for s in sources
            ],
            top_domains=[
                {"domain": s.domain, "count": s.citation_count}
                for s in sources[:10]
            ],
            by_type=by_type,
            by_source_type=by_source_type,
            period=f"Last {days} days",
        )
    
    # ========================================
    # Website Analysis
    # ========================================
    
    async def analyze_website(
        self,
        db: AsyncSession,
        url: str,
        depth: int = 1,
        force_refresh: bool = False,
    ) -> WebsiteAnalysisResponse:
        """
        Analyze a website for AI citation presence.
        
        Args:
            db: Database session
            url: Website URL to analyze
            depth: Number of pages to analyze
            force_refresh: Bypass cache
            
        Returns:
            Analysis results or status
        """
        domain = extract_domain_from_url(url) or url
        
        # Check for existing recent analysis
        if not force_refresh:
            cache_cutoff = datetime.utcnow() - timedelta(hours=24)
            existing_result = await db.execute(
                select(WebsiteAnalysis)
                .where(WebsiteAnalysis.domain == domain)
                .where(WebsiteAnalysis.status == AnalysisStatus.COMPLETED.value)
                .where(WebsiteAnalysis.completed_at >= cache_cutoff)
                .order_by(desc(WebsiteAnalysis.completed_at))
                .limit(1)
            )
            cached = existing_result.scalar_one_or_none()
            if cached:
                return self._build_analysis_response(cached)
        
        # Create new analysis
        analysis = WebsiteAnalysis(
            url=url,
            domain=domain,
            depth=depth,
            status=AnalysisStatus.PROCESSING.value,
            progress=10,
        )
        db.add(analysis)
        await db.flush()
        
        # Perform analysis (simplified for MVP)
        try:
            # Find citations for this domain
            citations_result = await db.execute(
                select(Citation)
                .where(Citation.source_domain == domain)
                .order_by(desc(Citation.created_at))
                .limit(100)
            )
            domain_citations = citations_result.scalars().all()
            
            # Get source info
            source_result = await db.execute(
                select(CitationSource)
                .where(CitationSource.normalized_domain == normalize_domain(domain))
            )
            source = source_result.scalar_one_or_none()
            
            # Build citation contexts
            contexts = []
            for citation in domain_citations[:10]:
                # Get conversation for context
                if citation.conversation_id:
                    conv_result = await db.execute(
                        select(Conversation).where(Conversation.id == citation.conversation_id)
                    )
                    conv = conv_result.scalar_one_or_none()
                    if conv:
                        contexts.append({
                            "query": conv.initial_query[:200] if conv.initial_query else "",
                            "response_snippet": citation.context[:200],
                            "sentiment": 0.0,  # TODO: Add sentiment
                            "citation_type": citation.citation_type,
                            "platform": conv.platform if conv.platform else None,
                            "timestamp": citation.created_at.isoformat(),
                        })
            
            # Generate recommendations
            recommendations = self._generate_recommendations(
                domain, len(domain_citations), source
            )
            
            # Update analysis
            analysis.status = AnalysisStatus.COMPLETED.value
            analysis.progress = 100
            analysis.citation_count = len(domain_citations)
            analysis.avg_sentiment = source.avg_sentiment if source else 0.0
            analysis.citation_contexts_json = json.dumps(contexts)
            analysis.recommendations_json = json.dumps([r.model_dump() for r in recommendations])
            analysis.pages_analyzed = 1
            analysis.completed_at = datetime.utcnow()
            
        except Exception as e:
            analysis.status = AnalysisStatus.FAILED.value
            analysis.error_message = str(e)
            analysis.completed_at = datetime.utcnow()
        
        await db.commit()
        await db.refresh(analysis)
        
        return self._build_analysis_response(analysis)
    
    def _build_analysis_response(self, analysis: WebsiteAnalysis) -> WebsiteAnalysisResponse:
        """Build response from analysis model."""
        contexts = []
        if analysis.citation_contexts_json:
            try:
                raw_contexts = json.loads(analysis.citation_contexts_json)
                contexts = [
                    CitationContextItem(
                        query=c.get("query", ""),
                        response_snippet=c.get("response_snippet", ""),
                        sentiment=c.get("sentiment", 0.0),
                        citation_type=c.get("citation_type", ""),
                        platform=c.get("platform"),
                        timestamp=datetime.fromisoformat(c["timestamp"]) if c.get("timestamp") else datetime.utcnow(),
                    )
                    for c in raw_contexts
                ]
            except (json.JSONDecodeError, KeyError):
                pass
        
        recommendations = []
        if analysis.recommendations_json:
            try:
                raw_recs = json.loads(analysis.recommendations_json)
                recommendations = [
                    WebsiteRecommendation(**r)
                    for r in raw_recs
                ]
            except (json.JSONDecodeError, KeyError):
                pass
        
        return WebsiteAnalysisResponse(
            id=analysis.id,
            url=analysis.url,
            domain=analysis.domain,
            status=analysis.status,
            progress=analysis.progress,
            citation_count=analysis.citation_count,
            avg_sentiment=analysis.avg_sentiment,
            citation_contexts=contexts,
            recommendations=recommendations,
            pages_analyzed=analysis.pages_analyzed,
            started_at=analysis.started_at,
            completed_at=analysis.completed_at,
            error_message=analysis.error_message,
        )
    
    def _generate_recommendations(
        self,
        domain: str,
        citation_count: int,
        source: Optional[CitationSource],
    ) -> List[WebsiteRecommendation]:
        """Generate optimization recommendations based on analysis."""
        recommendations = []
        
        # Always recommend llms.txt
        recommendations.append(WebsiteRecommendation(
            category="technical",
            title="Create llms.txt file",
            description="Add an llms.txt file to guide AI systems on how to index and reference your content. This emerging standard helps AI understand your site structure.",
            priority="P0",
            impact="high",
            effort="low",
        ))
        
        # Structured data
        recommendations.append(WebsiteRecommendation(
            category="technical",
            title="Implement Schema.org markup",
            description="Add structured data (JSON-LD) to help AI systems better understand your content, products, and organization.",
            priority="P0",
            impact="high",
            effort="medium",
        ))
        
        # Citation-based recommendations
        if citation_count == 0:
            recommendations.append(WebsiteRecommendation(
                category="content",
                title="Create authoritative content",
                description="Your site has no AI citations yet. Focus on creating comprehensive, factual content that AI systems would want to reference.",
                priority="P0",
                impact="high",
                effort="high",
            ))
        elif citation_count < 10:
            recommendations.append(WebsiteRecommendation(
                category="content",
                title="Expand content coverage",
                description=f"Your site has {citation_count} citations. Expand coverage of topics where you have expertise to increase AI references.",
                priority="P1",
                impact="medium",
                effort="medium",
            ))
        
        # FAQ section
        recommendations.append(WebsiteRecommendation(
            category="content",
            title="Add comprehensive FAQ",
            description="Create a detailed FAQ section that directly answers common questions in your domain. AI systems often pull from FAQ content.",
            priority="P1",
            impact="medium",
            effort="low",
        ))
        
        # Authority building
        if source and source.authority_score < 60:
            recommendations.append(WebsiteRecommendation(
                category="seo",
                title="Build domain authority",
                description="Your domain authority score is below average. Focus on earning backlinks from reputable sources and creating expert content.",
                priority="P1",
                impact="high",
                effort="high",
            ))
        
        return recommendations
    
    async def get_analysis_status(
        self,
        db: AsyncSession,
        analysis_id: int,
    ) -> Optional[AnalysisStatusResponse]:
        """Get status of website analysis."""
        result = await db.execute(
            select(WebsiteAnalysis).where(WebsiteAnalysis.id == analysis_id)
        )
        analysis = result.scalar_one_or_none()
        
        if not analysis:
            return None
        
        response = None
        if analysis.status == AnalysisStatus.COMPLETED.value:
            response = self._build_analysis_response(analysis)
        
        estimated_time = None
        if analysis.status == AnalysisStatus.PROCESSING.value:
            estimated_time = max(0, 30 - analysis.progress // 3)
        
        return AnalysisStatusResponse(
            id=analysis.id,
            status=analysis.status,
            progress=analysis.progress,
            estimated_time_seconds=estimated_time,
            result=response,
        )
    
    # ========================================
    # Statistics
    # ========================================
    
    async def get_stats(self, db: AsyncSession) -> CitationStatsResponse:
        """Get overall citation statistics."""
        # Total citations
        total_citations = await db.scalar(select(func.count(Citation.id))) or 0
        
        # Total sources
        total_sources = await db.scalar(select(func.count(CitationSource.id))) or 0
        
        # Total analyses
        total_analyses = await db.scalar(select(func.count(WebsiteAnalysis.id))) or 0
        
        # By source type
        source_type_result = await db.execute(
            select(CitationSource.source_type, func.count(CitationSource.id))
            .group_by(CitationSource.source_type)
        )
        top_source_types = {row[0]: row[1] for row in source_type_result.all()}
        
        # By citation type
        citation_type_result = await db.execute(
            select(Citation.citation_type, func.count(Citation.id))
            .group_by(Citation.citation_type)
        )
        top_citation_types = {row[0]: row[1] for row in citation_type_result.all()}
        
        # Average authority
        avg_authority = await db.scalar(
            select(func.avg(CitationSource.authority_score))
        ) or 0.0
        
        # Recent citations (24h)
        recent_cutoff = datetime.utcnow() - timedelta(hours=24)
        recent_count = await db.scalar(
            select(func.count(Citation.id))
            .where(Citation.created_at >= recent_cutoff)
        ) or 0
        
        return CitationStatsResponse(
            total_citations=total_citations,
            total_sources=total_sources,
            total_analyses=total_analyses,
            top_source_types=top_source_types,
            top_citation_types=top_citation_types,
            avg_authority_score=round(avg_authority, 1),
            recent_citations_count=recent_count,
        )


# Global service instance
citation_service = CitationService()
