import {
    Many2ManyBinaryField,
    many2ManyBinaryField,
} from "@web/views/fields/many2many_binary/many2many_binary_field";
import {ConfirmationDialog} from "@web/core/confirmation_dialog/confirmation_dialog";
import {_t} from "@web/core/l10n/translation";
import {registry} from "@web/core/registry";
import {useService} from "@web/core/utils/hooks";

/**
 * Many2many binary field for the e-invoice attachments.
 *
 * The standard widget uploads the files as attachments of the invoice, and
 * `account` then tries to import every attachment of an invoice as a document
 * (`_extend_with_attachments`): an XML could add lines to the invoice, and on
 * a new invoice (res_id = 0) the upload fails. Files are uploaded without a
 * linked record instead, and the server links them to the invoice on save.
 *
 * Removing a file asks for a confirmation: on save, the server deletes the
 * files of the invoice that are no longer listed.
 *
 * The files of the invoice have a description, exported in the XML: files of
 * other records do not, because their description is shared and often holds
 * internal texts.
 */
export class DocAttachmentsField extends Many2ManyBinaryField {
    static template = "l10n_it_edi_extension.DocAttachmentsField";

    setup() {
        super.setup();
        this.dialog = useService("dialog");
    }

    get files() {
        return this.props.record.data[this.props.name].records.map((record) => ({
            ...record.data,
            id: record.resId,
            record,
        }));
    }

    get descriptionTitle() {
        return _t("Description in the e-invoice XML");
    }

    isOwnFile(file) {
        // Not linked yet (uploaded before saving) or linked to this invoice
        const resId = file.res_id && file.res_id.resId;
        return (
            !resId ||
            (file.res_model === this.props.record.resModel &&
                resId === this.props.record.resId)
        );
    }

    getDefaultDescription(file) {
        return file.name.replace(/\.[^.]*$/, "");
    }

    onDescriptionChange(file, ev) {
        file.record.update({description: ev.target.value.trim()});
    }

    async onFileRemove(deleteId) {
        const file = this.files.find((f) => f.id === deleteId);
        this.dialog.add(ConfirmationDialog, {
            title: _t("Remove e-invoice attachment"),
            body: _t(
                'Remove "%s" from the e-invoice attachments? When the invoice is saved, the file is deleted, unless other records use it.',
                file ? file.name : ""
            ),
            confirmLabel: _t("Remove"),
            confirm: () => super.onFileRemove(deleteId),
            cancel: () => {
                // Keep the file in the list
            },
        });
    }
}

export const docAttachmentsField = {
    ...many2ManyBinaryField,
    component: DocAttachmentsField,
    relatedFields: [
        ...many2ManyBinaryField.relatedFields,
        // Related fields are readonly unless stated otherwise
        {name: "description", type: "text", readonly: false},
        {name: "res_model", type: "char"},
        {name: "res_id", type: "many2one_reference"},
    ],
};

registry.category("fields").add("l10n_it_edi_ext_doc_attachments", docAttachmentsField);
