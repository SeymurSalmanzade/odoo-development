from odoo import models
from odoo.tools import format_date
from datetime import datetime
import pytz
from odoo.exceptions import UserError
from lxml import etree

class CUSTOMCommon(models.AbstractModel):
    _name = 'custom.common'
    _description = 'Common Utility Functions for Addons'

    def _get_current_datetime(self, datetime_format='%d.%m.%Y %H-%M'):
        return datetime.now(pytz.timezone(self.env.user.tz or 'UTC')).strftime(datetime_format)

    def _get_format_date(self, date_field, date_format='dd MMMM yyyy'):
        return format_date(self.env, date_field, date_format=date_format)
    
    def _get_print_report_name(self, NAME=None):
        current_datetime = self._get_current_datetime()
        return f"{NAME} {current_datetime}"

    def _number_to_word_az(self, num_str, leading_zeros=False):
        num_str = str(num_str)
        if '.' in num_str:
            integer_part, decimal_part = num_str.split('.')
            if len(decimal_part) == 1 and int(decimal_part) > 0:
                decimal_part += "0"
            integer_words = self._number_to_word_az(integer_part)
            decimal_words = self._number_to_word_az(decimal_part) if int(decimal_part) > 0 else ''
            return f"{integer_words}, {decimal_words}" if int(decimal_part) > 0 else integer_words
        
        else:
            DIGITS = {
                        0: u"sıfır",
                        1: u"bir",
                        2: u"iki",
                        3: u"üç",
                        4: u"dörd",
                        5: u"beş",
                        6: u"altı",
                        7: u"yeddi",
                        8: u"səkkiz",
                        9: u"doqquz",
            }
                
            DECIMALS = {
                        1: u"on",
                        2: u"iyirmi",
                        3: u"otuz",
                        4: u"qırx",
                        5: u"əlli",
                        6: u"altmış",
                        7: u"yetmiş",
                        8: u"səksən",
                        9: u"doxsan",
            }

            POWERS_OF_TEN = {
                        2: u"yüz",
                        3: u"min",
                        6: u"milyon",
                        9: u"milyard",
                        12: u"trilyon",
                        15: u"katrilyon",
                        18: u"kentilyon",
                        21: u"sekstilyon",
                        24: u"septilyon",
                        27: u"oktilyon",
                        30: u"nonilyon",
                        33: u"desilyon",
                        36: u"undesilyon",
                        39: u"dodesilyon",
                        42: u"tredesilyon",
                        45: u"katordesilyon",
                        48: u"kendesilyon",
                        51: u"seksdesilyon",
                        54: u"septendesilyon",
                        57: u"oktodesilyon",
                        60: u"novemdesilyon",
                        63: u"vigintilyon",
            }
            
            words = []
            reversed_str = list(reversed(num_str))

            for index, digit in enumerate(reversed_str):
                digit_int = int(digit)
                remainder_to_3 = index % 3
                if remainder_to_3 == 0:
                    if index > 0:
                        if set(reversed_str[index:index+3]) != {'0'}:
                            words.insert(0, POWERS_OF_TEN[index])
                    if digit_int > 0:
                        words.insert(0, DIGITS[digit_int])
                elif remainder_to_3 == 1:
                    if digit_int != 0:
                        words.insert(0, DECIMALS[digit_int])
                else:
                    if digit_int > 0:
                        words.insert(0, POWERS_OF_TEN[2])
                    if digit_int > 1:
                        words.insert(0, DIGITS[digit_int])

            if num_str == '0':
                words.append(DIGITS[0])

            if leading_zeros:
                zeros_count = len(num_str) - len(str(int(num_str)))
                words[:0] = zeros_count * [DIGITS[0]]

            return " ".join(words)
        
    def _amount_to_word_az(self, amount):
        currency_unit_label = self.currency_id.currency_unit_label
        currency_subunit_label = self.currency_id.currency_subunit_label
        amount = str(amount)
        integer_part, decimal_part = amount.split('.')
        if len(decimal_part) == 1 and int(decimal_part) > 0:
            decimal_part += "0"
        integer_words = self._number_to_word_az(integer_part)
        decimal_words = self._number_to_word_az(decimal_part) if int(decimal_part) > 0 else ''
        if int(decimal_part) > 0:
            return f"{integer_words} {currency_unit_label}, {decimal_words} {currency_subunit_label}"
        else:
            return f"{integer_words} {currency_unit_label}"
        
    def render_custom_template(self, record, template_field):
        """Render the custom template content from the text field as a QWeb template."""
        qweb = self.env['ir.qweb']
        
        # Define the context with variables you want to pass to the QWeb template
        qweb_context = {
            'doc': record,
        }

        try:
            template_etree = etree.XML(template_field.encode('utf-8'))
        except Exception as e:
            raise UserError(f"Error parsing template content: {str(e)}")

        # Render the template from the content of the text field
        try:
            rendered_content = qweb._render(template_etree, qweb_context)
        except Exception as e:
            # Handle rendering errors (e.g., malformed QWeb syntax)
            raise UserError(f"Error rendering template: {str(e)}")
        
        return rendered_content
