"""Evidence Inspection Interface for VoiceOps 2026 (Hybrid Retrieval & RRF)."""
from typing import List, Dict, Any
from .retriever import HybridRRFRetriever


class EvidenceInspector:
    def __init__(self, retriever: HybridRRFRetriever):
        self.retriever = retriever

    def inspect_query(self, query: str, top_k: int = 5) -> str:
        results = self.retriever.retrieve_with_provenance(query, top_k=top_k)

        lines = [
            "=" * 80,
            f"  EVIDENCE PROVENANCE INSPECTOR — QUERY: '{query}'",
            "=" * 80,
            f"{'Rank':<5} | {'Section ID':<12} | {'BM25 Rank':<10} | {'Dense Rank':<10} | {'RRF Score':<10} | {'Final Score':<10}",
            "-" * 80
        ]

        for rank, item in enumerate(results, start=1):
            sec = item['section']
            r_lex = str(item['lexical_rank']) if item['lexical_rank'] < 9999 else "None"
            r_dense = str(item['dense_rank']) if item['dense_rank'] < 9999 else "None"
            rrf = f"{item['rrf_score']:.5f}"
            final = f"{item['final_score']:.5f}"

            lines.append(f"{rank:<5} | {sec.section_id:<12} | {r_lex:<10} | {r_dense:<10} | {rrf:<10} | {final:<10}")
            lines.append(f"      Title: {sec.doc_title} -> {sec.heading} ({sec.doc_type}, {sec.doc_status})")
            snippet = sec.content.replace('\n', ' ')[:90] + "..." if len(sec.content) > 90 else sec.content
            lines.append(f"      Snippet: {snippet}")
            lines.append("-" * 80)

        return "\n".join(lines)
