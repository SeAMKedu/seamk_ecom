# SeAMK eCommerce

## Description

A custom Odoo module that adds an extra step to the Odoo online shop.

If the shopping cart contains a product called 'Support', the module extends the default checkout process by adding an extra page for a customer to set the input parameters of the support: the distances of the 3 holes and a force (weight) that is affecting to the support. These input parameters are sent to the REST API of the external MES application. After a FEA (Finite Element Analysis) is done, the API returns the following parameters: R1, R2, area, and stress. Both inputs and results of the FEA are stored to the field 'x_fea_params' of the sale order record.

The module also fetches the geometry of the support as a PNG image file. A third request to the API returns the geometry of the support as a binary data which is stored to the custom field 'x_fea_image' of the sale order record.

## Acknowledgment

This module was developed as a part of the Enterprise Digital Twin Platform (EDIT) project, which is funded by Pirkanmaan liitto and EAKR.

Project description in Finnish: [Enterprise Digital Twin Platform](https://www.seamk.fi/yrityksille/tki-projektit/projektitietokanta/?RepoProject=411045).