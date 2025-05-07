from io import BytesIO
from fastapi import UploadFile, HTTPException
from typing import List
from shared.utils.indexing.process_file import (
    load_docx_from_file,
    load_excel_from_file,
    load_pdf_from_file,
    load_txt_from_file,
)


def process_file(file: UploadFile) -> List[str]:
    """
    Xử lý file tải lên và trả về nội dung dưới dạng danh sách chuỗi.

    Args:
        file (UploadFile): File tải lên từ người dùng.

    Returns:
        List[str]: Nội dung file dưới dạng danh sách chuỗi.

    Raises:
        HTTPException: Nếu file không được hỗ trợ hoặc bị lỗi.
    """
    contents = file.file.read()
    print(f"📂 Đọc được {len(contents)} bytes từ file {file.filename}")

    if not contents:
        raise HTTPException(
            status_code=400, detail="Lỗi đọc file! File có thể bị hỏng."
        )

    file_extension = file.filename.split(".")[-1].lower()
    file_obj = BytesIO(contents)

    file_handlers = {
        "pdf": load_pdf_from_file,
        "docx": load_docx_from_file,
        "txt": load_txt_from_file,
        "xls": load_excel_from_file,
        "xlsx": load_excel_from_file,
    }

    if file_extension not in file_handlers:
        raise HTTPException(status_code=400, detail="Định dạng file không được hỗ trợ!")

    return file_handlers[file_extension](file_obj)
