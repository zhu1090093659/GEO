"""
Optimization Module - Business Logic Service
"""

from datetime import datetime
from typing import List, Optional
import uuid

from .models import Recommendation, LlmsTxtResult
from .schemas import (
    RecommendationsResponse,
    RecommendationItem,
    LlmsTxtResponse,
)


# llms.txt template
LLMS_TXT_TEMPLATE = """# {site_name}

> {description}

## About

{about}

## Main Sections

{sections}

## Key Topics

{topics}

## Contact

- Website: {url}
{contact}
"""


class OptimizationService:
    """Service for optimization recommendations and llms.txt generation"""

    def __init__(self):
        # In-memory storage for MVP
        self._recommendations: List[Recommendation] = []
        self._llms_txt_results: dict[str, LlmsTxtResult] = {}

    async def generate_recommendations(
        self,
        brand: str,
        focus_areas: Optional[List[str]] = None,
    ) -> RecommendationsResponse:
        """
        Generate optimization recommendations for a brand.
        
        Args:
            brand: Brand name
            focus_areas: Optional areas to focus on
            
        Returns:
            List of actionable recommendations
        """
        # Generate recommendations based on analysis
        # TODO: Integrate with Agent for intelligent recommendations
        recommendations = [
            Recommendation(
                id=str(uuid.uuid4()),
                brand=brand,
                category="content",
                priority="P0",
                title="Improve Product Descriptions",
                description="AI assistants often cite detailed product descriptions. Enhance your product pages with comprehensive, factual information.",
                action_steps=[
                    "Review current product descriptions for completeness",
                    "Add specific features, specifications, and use cases",
                    "Include comparison points with alternatives",
                    "Add structured data markup (schema.org)",
                ],
                expected_impact="15-20% improvement in visibility score",
                effort="medium",
            ),
            Recommendation(
                id=str(uuid.uuid4()),
                brand=brand,
                category="content",
                priority="P0",
                title="Create Comprehensive FAQ Section",
                description="FAQs closely match how users query AI assistants. Create content that directly answers common questions.",
                action_steps=[
                    "Identify top queries related to your brand from Topic Discovery",
                    "Create detailed answers for each question",
                    "Use natural language that AI can easily extract",
                    "Update FAQ regularly based on new trends",
                ],
                expected_impact="10-15% improvement in citation rate",
                effort="low",
            ),
            Recommendation(
                id=str(uuid.uuid4()),
                brand=brand,
                category="technical",
                priority="P0",
                title="Add llms.txt File",
                description="Create and deploy llms.txt to help AI assistants better understand and index your content.",
                action_steps=[
                    "Use GEO llms.txt generator to create the file",
                    "Review and customize the generated content",
                    "Deploy to your website root (/llms.txt)",
                    "Keep updated as content changes",
                ],
                expected_impact="20-30% improvement in AI discoverability",
                effort="low",
            ),
            Recommendation(
                id=str(uuid.uuid4()),
                brand=brand,
                category="structure",
                priority="P1",
                title="Implement Schema.org Markup",
                description="Structured data helps AI understand your content context and relationships.",
                action_steps=[
                    "Add Organization schema to homepage",
                    "Add Product schema to product pages",
                    "Add FAQ schema to FAQ pages",
                    "Validate markup with Google's testing tool",
                ],
                expected_impact="10-15% improvement in structured citations",
                effort="medium",
            ),
            Recommendation(
                id=str(uuid.uuid4()),
                brand=brand,
                category="content",
                priority="P1",
                title="Publish Authoritative Content",
                description="Create expert content that AI assistants are more likely to cite as authoritative sources.",
                action_steps=[
                    "Identify topics where you have expertise",
                    "Create in-depth guides and tutorials",
                    "Include data, research, and citations",
                    "Keep content updated and accurate",
                ],
                expected_impact="Long-term authority building",
                effort="high",
            ),
        ]

        # Filter by focus areas if specified
        if focus_areas:
            recommendations = [r for r in recommendations if r.category in focus_areas]

        # Store recommendations
        self._recommendations.extend(recommendations)

        # Build summary
        summary = {
            "total": len(recommendations),
            "by_priority": {
                "P0": len([r for r in recommendations if r.priority == "P0"]),
                "P1": len([r for r in recommendations if r.priority == "P1"]),
                "P2": len([r for r in recommendations if r.priority == "P2"]),
            },
            "by_category": {
                "content": len([r for r in recommendations if r.category == "content"]),
                "structure": len([r for r in recommendations if r.category == "structure"]),
                "technical": len([r for r in recommendations if r.category == "technical"]),
            },
        }

        return RecommendationsResponse(
            brand=brand,
            generated_at=datetime.utcnow(),
            recommendations=[
                RecommendationItem(
                    id=r.id,
                    category=r.category,
                    priority=r.priority,
                    title=r.title,
                    description=r.description,
                    action_steps=r.action_steps,
                    expected_impact=r.expected_impact,
                    effort=r.effort,
                    status=r.status,
                )
                for r in recommendations
            ],
            summary=summary,
        )

    async def get_recommendations(self, brand: str) -> List[RecommendationItem]:
        """Get existing recommendations for a brand"""
        return [
            RecommendationItem(
                id=r.id,
                category=r.category,
                priority=r.priority,
                title=r.title,
                description=r.description,
                action_steps=r.action_steps,
                expected_impact=r.expected_impact,
                effort=r.effort,
                status=r.status,
            )
            for r in self._recommendations
            if r.brand.lower() == brand.lower()
        ]

    async def update_recommendation_status(
        self,
        recommendation_id: str,
        status: str,
    ) -> bool:
        """Update recommendation status"""
        for r in self._recommendations:
            if r.id == recommendation_id:
                r.status = status
                return True
        return False

    async def generate_llms_txt(
        self,
        url: str,
        site_name: str,
        description: Optional[str] = None,
        auto_generate: bool = True,
        sections: Optional[List[dict]] = None,
    ) -> LlmsTxtResponse:
        """
        Generate llms.txt content for a website.
        
        Args:
            url: Website URL
            site_name: Site/organization name
            description: Optional description
            auto_generate: Whether to auto-discover sections
            sections: Optional predefined sections
            
        Returns:
            Generated llms.txt content
        """
        result_id = str(uuid.uuid4())

        # Auto-generate description if not provided
        if not description:
            description = f"Official website for {site_name}"

        # Generate about section
        about = f"{site_name} provides comprehensive information and resources."

        # Generate sections list
        if sections:
            sections_text = "\n".join([
                f"- [{s.get('name', 'Section')}]({s.get('path', '/')}): {s.get('description', '')}"
                for s in sections
            ])
        else:
            # Default sections
            sections_text = """- [Home](/): Main landing page
- [Products](/products): Our product offerings
- [About](/about): About our company
- [Blog](/blog): Latest news and insights
- [Contact](/contact): Get in touch"""

        # Generate topics
        topics_text = "- Product information\n- Company updates\n- Industry insights"

        # Build content
        content = LLMS_TXT_TEMPLATE.format(
            site_name=site_name,
            description=description,
            about=about,
            sections=sections_text,
            topics=topics_text,
            url=url,
            contact="",
        )

        # Store result
        result = LlmsTxtResult(
            id=result_id,
            url=url,
            content=content,
            preview_url=f"/api/optimization/llms-txt/{result_id}/preview",
            download_url=f"/api/optimization/llms-txt/{result_id}/download",
        )
        self._llms_txt_results[result_id] = result

        sections_count = len(sections) if sections else 5

        return LlmsTxtResponse(
            url=url,
            content=content,
            preview_url=result.preview_url,
            download_url=result.download_url,
            sections_count=sections_count,
            created_at=result.created_at,
        )

    async def get_llms_txt(self, result_id: str) -> Optional[LlmsTxtResult]:
        """Get generated llms.txt by ID"""
        return self._llms_txt_results.get(result_id)


# Global service instance
optimization_service = OptimizationService()
