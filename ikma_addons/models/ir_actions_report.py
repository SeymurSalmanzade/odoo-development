from odoo import models
import io
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import letter
from odoo.tools.pdf import PdfFileReader, PdfFileWriter
import base64


class IrActionsReport(models.Model):
    _inherit = 'ir.actions.report'

    def _render_qweb_pdf(self,report_ref,res_ids=None,data=None):
        #override base method for contract raw template
        pdf_content, content_type = super(IrActionsReport, self)._render_qweb_pdf(report_ref, res_ids=res_ids, data=data)
        if report_ref in ('ikma_addons.contract_template_raw', 'ikma_addons.tta_raw'):
            pdf_reader = PdfFileReader(io.BytesIO(pdf_content))
            total_pages_count = len(pdf_reader.pages)
            pdf_with_page_number_alignment = io.BytesIO()
            pdf_writer = PdfFileWriter()
            for i in range(total_pages_count):
                # Get original page
                page = pdf_reader.getPage(i) # Get the page [i]
                pdf_writer.addPage(page) # Add the page to the writer

                packet = io.BytesIO()
                # Use a Canvas and draw (Page 1 of 9(example)) to right coordinates in pages
                canva = Canvas(packet,pagesize = letter)
                page_number_placeholder = f"{i+1} / {total_pages_count}"
                canva.drawString(550, 10, page_number_placeholder)
                canva.save()

                packet.seek(0)
                number_overlay = PdfFileReader(packet)
                # Merge the canvas
                page.mergePage(number_overlay.getPage(0))
            # Write the updated PDF to a BytesIO object
            pdf_writer.write(pdf_with_page_number_alignment)
            pdf_with_page_number_alignment.seek(0)
            return pdf_with_page_number_alignment.getvalue(), content_type

        return pdf_content, content_type

    def _render_qweb_pdf_prepare_streams(self, report_ref, data, res_ids=None):
        result = super()._render_qweb_pdf_prepare_streams(report_ref, data, res_ids=res_ids)
        if self._get_report(report_ref).report_name != 'ikma_addons.contract_template_raw':
            return result

        orders = self.env['sale.order'].browse(res_ids)

        for order in orders:
            initial_stream = result[order.id]['stream']
            if initial_stream:
                contract_headers = order.header_contract_attachment_ids
                contract_footers = order.footer_contract_attachment_ids
                writer = PdfFileWriter()
                if contract_headers:
                    for contract_header in contract_headers.sorted('sequence'):
                        self._add_pages_to_writer(writer, base64.b64decode(contract_header.datas))
                self._add_pages_to_writer(writer, initial_stream.getvalue())
                if contract_footers:
                    for contract_footer in contract_footers.sorted('sequence'):
                        self._add_pages_to_writer(writer, base64.b64decode(contract_footer.datas))
                with io.BytesIO() as _buffer:
                    writer.write(_buffer)
                    stream = io.BytesIO(_buffer.getvalue())
                result[order.id].update({'stream': stream})

        return result