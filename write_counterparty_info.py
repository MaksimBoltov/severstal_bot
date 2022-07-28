from fpdf import FPDF
from models import Counterparties


def generate_counterparty_report(counterparty: Counterparties) -> str:
    """Создает докуент с информацией по контрагенту и возвращает путь к файлу."""

    pdf = FPDF()
    pdf.add_page()

    # pdf.image('data/logo.png', x=180, y=12, w=10)

    pdf.add_font('DejaVu', '', 'font/DejaVuSansCondensed.ttf', uni=True)
    pdf.set_font('DejaVu', '', 14)
    pdf.cell(300, 10, txt=f'Информация по контрагенту "{counterparty.name}"', ln=1, align="L")
    pdf.cell(300, 10, txt=f"Наименование контрагента: {counterparty.name}", ln=1, align="L")
    pdf.cell(300, 10, txt=f"ИНН: {counterparty.inn}", ln=1, align="L")
    pdf.cell(300, 10, txt=f"Адрес: {counterparty.address}", ln=1, align="L")
    pdf.cell(300, 10, txt=f"Дата подписания договора: {counterparty.conclusion_contract_date}", ln=1, align="L")
    pdf.cell(300, 10, txt=f"Статус договора: {'Активен' if counterparty.active else 'Неактивен'}", ln=1, align="L")

    report_path = f"data/{counterparty.name}.pdf"
    pdf.output(report_path)
    pdf.close()

    return report_path
