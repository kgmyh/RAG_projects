"""
문서 로더 테스트
"""

import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

from src.document.loader import PDFLoader, load_pdf_documents


class TestPDFLoader:
    """PDFLoader 테스트"""

    def test_init_with_valid_path(self, tmp_path):
        """유효한 경로로 초기화 테스트"""
        # 임시 PDF 파일 생성
        pdf_file = tmp_path / "test.pdf"
        pdf_file.touch()

        loader = PDFLoader(pdf_file)
        assert loader.file_path == pdf_file

    def test_init_with_invalid_path(self):
        """잘못된 경로로 초기화 시 예외 발생 테스트"""
        with pytest.raises(FileNotFoundError):
            PDFLoader("/nonexistent/path/file.pdf")

    @patch("src.document.loader.PyPDFLoader")
    def test_load(self, mock_pypdf_loader, tmp_path):
        """PDF 로드 테스트"""
        # 임시 PDF 파일 생성
        pdf_file = tmp_path / "test.pdf"
        pdf_file.touch()

        # Mock 설정
        mock_doc = MagicMock()
        mock_doc.page_content = "테스트 내용"
        mock_doc.metadata = {}
        mock_instance = mock_pypdf_loader.return_value
        mock_instance.load.return_value = [mock_doc]

        loader = PDFLoader(pdf_file)
        documents = loader.load()

        assert len(documents) == 1
        assert documents[0].metadata["source"] == "test.pdf"
        assert documents[0].metadata["file_type"] == "pdf"


class TestLoadPDFDocuments:
    """load_pdf_documents 함수 테스트"""

    @patch("src.document.loader.PDFLoader")
    def test_load_multiple_pdfs(self, mock_loader_class, tmp_path):
        """여러 PDF 파일 로드 테스트"""
        # 임시 PDF 파일 생성
        (tmp_path / "test1.pdf").touch()
        (tmp_path / "test2.pdf").touch()

        # Mock 설정
        mock_doc = MagicMock()
        mock_doc.page_content = "테스트"
        mock_doc.metadata = {}
        mock_instance = mock_loader_class.return_value
        mock_instance.load.return_value = [mock_doc]

        documents = load_pdf_documents(tmp_path)

        assert mock_loader_class.call_count == 2
