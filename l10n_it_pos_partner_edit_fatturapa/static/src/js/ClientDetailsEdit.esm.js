// Copyright 2025 Martin Stecher - IT-S
const {useState} = owl;
import PartnerDetailsEdit from "point_of_sale.PartnerDetailsEdit";
import Registries from "point_of_sale.Registries";

const PartnerDetailsEditItaly = (OriginalPartnerDetailsEdit) =>
    class extends OriginalPartnerDetailsEdit {
        setup() {
            super.setup();
            this.changes = useState({
                ...this.changes,
                electornic_invoice_subjected:
                    this.props.partner.electornic_invoice_subjected || true,
                electronic_invoice_obliged_subject:
                    this.props.partner.electronic_invoice_obliged_subject || true,
                codice_destinatario: this.props.partner.codice_destinatario || null,
                pec_destinatario: this.props.partner.pec_destinatario || null,
            });
        }
    };

Registries.Component.extend(PartnerDetailsEdit, PartnerDetailsEditItaly);
