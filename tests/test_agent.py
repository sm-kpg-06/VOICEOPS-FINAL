"""Automated Test Suite for VoiceOps Support Agent (Hybrid Retrieval and Reranking)."""
import os
import unittest
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.knowledge_base import KnowledgeBase
from src.retriever import HybridRRFRetriever
from src.tools_adapter import ToolsAdapter
from src.conversation_agent import ConversationAgent
from src.evidence_inspector import EvidenceInspector


class TestAgent(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        cand1 = os.path.join(base_dir, 'Capstone_Project_Dataset_FTTT_2026')
        cand2 = os.path.join(os.path.dirname(base_dir), 'Capstone_Project_Dataset_FTTT_2026')
        cls.ds_dir = cand1 if os.path.isdir(cand1) else (cand2 if os.path.isdir(cand2) else 'Capstone_Project_Dataset_FTTT_2026')
        cls.kb = KnowledgeBase(cls.ds_dir)
        cls.retriever = HybridRRFRetriever(cls.kb, k_constant=60)
        cls.tools = ToolsAdapter(cls.ds_dir)
        cls.conv_agent = ConversationAgent(cls.kb, cls.tools, cls.retriever)
        cls.inspector = EvidenceInspector(cls.retriever)

    def test_rrf_provenance_and_fusion(self):
        """Verify RRF calculates ranks and scores from both lexical and dense branches."""
        results = self.retriever.retrieve_with_provenance("How fast are refunds to the ZentroMart Wallet?", top_k=5)
        self.assertGreater(len(results), 0)
        top = results[0]
        self.assertIn('lexical_rank', top)
        self.assertIn('dense_rank', top)
        self.assertIn('rrf_score', top)
        self.assertIn('final_score', top)
        # REF-2 should be top or in top 3
        top_ids = [item['section'].section_id for item in results[:3]]
        self.assertIn("REF-2", top_ids)

    def test_deduplication(self):
        """Ensure no duplicate sections appear in fused results."""
        results = self.retriever.retrieve_with_provenance("return policy shoes clothing", top_k=5)
        sec_ids = [item['section'].section_id for item in results]
        self.assertEqual(len(sec_ids), len(set(sec_ids)))

    def test_evidence_inspector_output(self):
        """Verify evidence inspector generates structured inspection table."""
        table_str = self.inspector.inspect_query("return window for clothing")
        self.assertIn("EVIDENCE PROVENANCE INSPECTOR", table_str)
        self.assertIn("BM25 Rank", table_str)
        self.assertIn("Dense Rank", table_str)
        self.assertIn("RRF Score", table_str)

    def test_identity_and_ticket_tools(self):
        """Verify verification gate and ticket escalation."""
        unverified = self.tools.lookup("89782837")
        self.assertTrue(unverified.get('verification_required'))

        verified = self.tools.lookup("89782837", verification_value="4533")
        self.assertTrue(verified.get('verified'))

        ticket = self.tools.ticket(
            summary="High value damaged item review required by priority resolution team.",
            order_id="89782837",
            reason="high_value_damage"
        )
        self.assertTrue(ticket.get('created'))

    def test_mocked_voice_adapter_pipeline(self):
        """[MOCKED UNIT TEST] Verify voice adapter audio processing workflow with mocked Gnani clients."""
        from unittest.mock import MagicMock
        from src.voice_adapter import GnaniVoiceAdapter
        mock_stt = MagicMock()
        mock_tts = MagicMock()
        mock_stt.transcribe.return_value = {"transcript": "What is the return window for clothing?"}
        mock_tts.synthesize.return_value = b"RIFFfakeaudio"

        voice = GnaniVoiceAdapter(self.conv_agent, stt_client=mock_stt, tts_client=mock_tts)
        self.assertTrue(voice.is_live)

        res = voice.process_voice_turn("/tmp/test_voice_turn.wav", conv_id="test_mock_voice")
        self.assertEqual(res['transcription'], "What is the return window for clothing?")
        self.assertEqual(res['stt_status'], "live_gnani_stt")
        self.assertIn("zentromart", res['reply_text'].lower())
        mock_tts.synthesize.assert_called_once()


if __name__ == '__main__':
    unittest.main()
