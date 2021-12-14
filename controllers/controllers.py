# -*- coding: utf-8 -*-
import json

from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale


class SeamkEcom(WebsiteSale):
    """SeAMK eCommerce"""

    def get_colors(self, code: str) -> tuple:
        """
        Get the colors of the components of the cell phone.

        Args:
            code (str): The internal reference code of the cell phone.

        Returns:
            (tuple): The color of the components.
        """
        # Conversion from number to color.
        cover = {"2": "Black", "3": "Blue", "4": "Gray", "5": "Red"}
        board = {"1": "Green", "3": "Blue", "5": "Red"}
        fuses = {"0": "None", "1": "Normal", "3": "Blue", "5": "Red"}

        c1 = cover[code[0]]
        c2 = board[code[1]]
        c3 = fuses[code[2]]
        c4 = fuses[code[3]]
        c5 = "None"

        return (c1, c2, c3, c4, c5)


    @http.route("/shop/extra", type="http", methods=["GET", "POST"], website=True, auth="public", csrf=False, cors="*")
    def extra(self, **kw):
        """Route for the extra step in the checkout process of the online shop."""
        # Product definitions.
        name_phone = "Cell Phone"
        name_support = "Support"
        partno_support = "70000"

        fea_image = b""
        fea_params = {}

        if request.httprequest.method == "GET":
            return request.render("seamk_ecom.extra")

        # The customer submitted the input and output params of the FEA.
        if request.httprequest.method == "POST":
            # Loop through the lines (i.e. products) in the sale order.
            sale_order = request.website.sale_get_order()
            for line in sale_order.order_line:
                name = line.product_template_id.name

                params = {}
                partno = ""  # part number of the product

                if name == name_phone:
                    code = line.product_id.code
                    colors = self.get_colors(code)
                    params = {
                        "cover": colors[0],
                        "board": colors[1],
                        "fuseL": colors[2],
                        "fuseR": colors[3],
                    }
                    partno = code

                elif name == name_support:
                    # Read the posted form data.
                    d_1 = int(request.params["d1"])
                    d_2 = int(request.params["d2"])
                    d_3 = int(request.params["d3"])
                    force = int(request.params["f"])
                    area = float(request.params["area"])
                    r_1 = float(request.params["r1"])
                    r_2 = float(request.params["r2"])
                    stress = float(request.params["stress"])
                    # Save the image data.
                    fea_image = request.params["imgdata"]

                    # Set a name of this specific support. The name is shown
                    # on the column 'Description' on the sale order form.
                    new_name = "[{}] {} ({}, {}, {}, {}, {}, {}, {}, {})".format(
                        partno_support, name_support,
                        d_1, d_2, d_3, force, r_1, r_2, area, stress
                    )
                    # Write the field of the sale order line.
                    field = {"name": new_name}
                    line.write(field)

                    # Inputs and outputs of the finite element analysis.
                    params = {
                        "d1": d_1,
                        "d2": d_2,
                        "d3": d_3,
                        "f": force,
                        "r1": r_1,
                        "r2": r_2,
                        "area": area,
                        "stress": stress
                    }
                    # Part number of the product. Will be used as a key in the
                    # product parameters dictionary.
                    partno = partno_support

                # In case of the cell phone, the product parameters contain
                # the colors of the components of the phone.
                # In case of the support, the product parameters contain the
                # input and output parameters of the finite element analysis.
                fea_params[partno] = params

            # Write the added custom fields of the sale order record.
            fields = {
                "x_fea_image": fea_image,
                "x_fea_params": json.dumps(fea_params)
            }
            sale_order.write(fields)

            #request.session["extra_info_done"] = True
            return request.redirect("/shop/payment")


    @http.route(["/shop/confirm_order"], type="http", website=True, auth="public", csrf=False, cors="*")
    def confirm_order(self, **post):
        """Redirects a customer to the added step."""
        #if not request.session.get("extra_info_done"):
        #    return request.redirect("/shop/extra")
        #return super(SeamkEcom, self).confirm_order(**post)
        return request.redirect("/shop/extra")
