"""
Citation Module - Business Logic Service
"""

from datetime import datetime
from typing import List, Optional
import re
import uuid

from .models import Citation, WebsiteAnalysis, CitationContext
from .schemas import (
    CitationDiscoveryResponse,
    CitationSourceItem,
    WebsiteAnalysisResponse,
    WebsiteRecommendation,
    CitationContextItem,
    AnalysisStatusResponse,
)


# URL extraction pattern
URL_PATTERN = re.compile(r'https?://[^\s<>"{}|\\^`\[\]]+')
DOMAIN_PATTERN = re.compile(r'(?:according to |source: |from )([a-zA-Z0-9][-a-zA-Z0-9]*(?:\.[a-zA-Z]{2,})+)', re.I)


class CitationService:
    """Service for citation discovery and website analysis"""

    def __init__(self):
        # In-memory storage for MVP
        self._citations: List[Citation] = []
        self._analyses: dict[str, WebsiteAnalysis] = {}

    def extract_citations_from_text(self, text: str, conversation_id: str) -> List[Citation]:
        """
        Extract citations from AI response text.
        
        Args:
            text: AI response text
            conversation_id: Associated conversation ID
            
        Returns:
            List of extracted citations
        """
        citations = []

        # Extract URLs
        for match in URL_PATTERN.finditer(text):
            url = match.group()
            domain = self._extract_domain(url)
            citation = Citation(
                id=str(uuid.uuid4()),
                conversation_id=conversation_id,
                source_url=url,
                source_domain=domain,
                citation_type="url",
                authority_score=self._calculate_authority(domain),
                context=self._get_context(text, match.start(), match.end()),
            )
            citations.append(citation)

        # Extract domain references
        for match in DOMAIN_PATTERN.finditer(text):
            domain = match.group(1)
            citation = Citation(
                id=str(uuid.uuid4()),
                conversation_id=conversation_id,
                source_domain=domain,
                citation_type="domain",
                authority_score=self._calculate_authority(domain),
                context=self._get_context(text, match.start(), match.end()),
            )
            citations.append(citation)

        self._citations.extend(citations)
        return citations

    def _extract_domain(self, url: str) -> str:
        """Extract domain from URL"""
        try:
            from urllib.parse import urlparse
            parsed = urlparse(url)
            return parsed.netloc
        except Exception:
            return url

    def _calculate_authority(self, domain: str) -> float:
        """Calculate authority score for a domain"""
        # Simple heuristic based on TLD
        if domain.endswith('.gov') or domain.endswith('.edu'):
            return 90.0
        elif any(news in domain for news in ['nytimes', 'bbc', 'reuters', 'cnn']):
            return 85.0
        elif 'wikipedia' in domain:
            return 75.0
        else:
            return 50.0

    def _get_context(self, text: str, start: int, end: int, window: int = 100) -> str:
        """Get surrounding context for a citation"""
        ctx_start = max(0, start - window)
        ctx_end = min(len(text), end + window)
        return text[ctx_start:ctx_end].strip()

    async def discover_citations(
        self,
        brand: Optional[str] = None,
        limit: int = 50,
    ) -> CitationDiscoveryResponse:
        """
        Discover citations from collected data.
        
        Args:
            brand: Optional brand filter
            limit: Maximum results
            
        Returns:
            Citation discovery results
        """
        # Group citations by source
        source_counts: dict = {}
        for citation in self._citations:
            source = citation.source_domain or citation.source_name or "unknown"
            if source not in source_counts:
                source_counts[source] = {
                    "count": 0,
                    "authority": citation.authority_score,
                    "type": citation.citation_type,
                    "context": citation.context,
                }
            source_counts[source]["count"] += 1

        # Build response
        sources = [
            CitationSourceItem(
                source=source,
                source_type=data["type"],
                citation_count=data["count"],
                authority_score=data["authority"],
                sample_context=data["context"][:200] if data["context"] else None,
            )
            for source, data in sorted(
                source_counts.items(),
                key=lambda x: x[1]["count"],
                reverse=True,
            )[:limit]
        ]

        # Count by type
        by_type = {}
        for citation in self._citations:
            t = citation.citation_type
            by_type[t] = by_type.get(t, 0) + 1

        return CitationDiscoveryResponse(
            total_citations=len(self._citations),
            sources=sources,
            top_domains=[{"domain": s.source, "count": s.citation_count} for s in sources[:10]],
            by_type=by_type,
        )

    async def analyze_website(self, url: str, depth: int = 1) -> WebsiteAnalysisResponse:
        """
        Start website analysis for citation presence.
        
        Args:
            url: Website URL to analyze
            depth: Number of pages to analyze
            
        Returns:
            Analysis initiation response
        """
        analysis_id = str(uuid.uuid4())
        domain = self._extract_domain(url)

        # Create analysis record
        analysis = WebsiteAnalysis(
            id=analysis_id,
            url=url,
            domain=domain,
            status="processing",
        )
        self._analyses[analysis_id] = analysis

        # Find citations for this domain (simulated)
        domain_citations = [c for c in self._citations if c.source_domain == domain]

        # Calculate metrics
        citation_count = len(domain_citations)
        avg_sentiment = 0.5  # Placeholder

        # Generate recommendations
        recommendations = [
            WebsiteRecommendation(
                category="content",
                title="Add Structured Data",
                description="Implement schema.org markup to help AI better understand your content.",
                priority="P0",
            ),
            WebsiteRecommendation(
                category="technical",
                title="Create llms.txt",
                description="Add llms.txt file to guide AI indexing of your content.",
                priority="P0",
            ),
            WebsiteRecommendation(
                category="content",
                title="Improve FAQ Section",
                description="Add comprehensive FAQ to match common AI queries.",
                priority="P1",
            ),
        ]

        # Update analysis
        analysis.status = "completed"
        analysis.citation_count = citation_count
        analysis.avg_sentiment = avg_sentiment
        analysis.recommendations = [r.title for r in recommendations]
        analysis.completed_at = datetime.utcnow()

        return WebsiteAnalysisResponse(
            url=url,
            status="completed",
            analysis_id=analysis_id,
            citation_count=citation_count,
            sentiment_avg=avg_sentiment,
            citation_contexts=[],
            recommendations=recommendations,
            completed_at=analysis.completed_at,
        )

    async def get_analysis_status(self, analysis_id: str) -> Optional[AnalysisStatusResponse]:
        """Get status of website analysis"""
        analysis = self._analyses.get(analysis_id)
        if not analysis:
            return None

        result = None
        if analysis.status == "completed":
            result = WebsiteAnalysisResponse(
                url=analysis.url,
                status=analysis.status,
                analysis_id=analysis_id,
                citation_count=analysis.citation_count,
                sentiment_avg=analysis.avg_sentiment,
                citation_contexts=[],
                recommendations=[
                    WebsiteRecommendation(
                        category="content",
                        title=r,
                        description="",
                        priority="P1",
                    )
                    for r in analysis.recommendations
                ],
                completed_at=analysis.completed_at,
            )

        return AnalysisStatusResponse(
            analysis_id=analysis_id,
            status=analysis.status,
            progress=100 if analysis.status == "completed" else 50,
            estimated_time=0 if analysis.status == "completed" else 30,
            result=result,
        )


# Global service instance
citation_service = CitationService()
