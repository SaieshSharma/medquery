from pathlib import Path
import xml.etree.ElementTree as ET

from medquery.schemas.document import Document


def load_medquad(data_dir: Path,require_answers: bool = True,
) -> list[Document]:
    documents: list[Document] = []

    for xml_file in data_dir.rglob("*.xml"):
        tree = ET.parse(xml_file)
        root = tree.getroot()

        source = root.get("source", "")
        url = root.get("url", "")
        focus = root.findtext("Focus", default="").strip()

        for qa_pair in root.findall(".//QAPair"):
            question_element = qa_pair.find("Question")
            answer_element = qa_pair.find("Answer")

            if question_element is None:
                continue

            question = (question_element.text or "").strip()
            answer = (
                (answer_element.text or "").strip()
                if answer_element is not None
                else ""
            )
            if require_answers and not answer:
                continue
            if not question:
                continue

            qid = question_element.get("qid", "")
            qtype = question_element.get("qtype", "")

            text_parts = [
                f"Question: {question}",
            ]

            if answer:
                text_parts.append(f"Answer: {answer}")

            if focus:
                text_parts.append(f"Focus: {focus}")

            documents.append(
                Document(
                    text="\n".join(text_parts),
                    source="medquad",
                    document_id=qid,
                    metadata={
                        "source_name": source,
                        "url": url,
                        "focus": focus,
                        "question_type": qtype,
                        "file": str(xml_file),
                    },
                )
            )

    return documents