import {Component} from "@odoo/owl";
import {FileModel} from "@web/core/file_viewer/file_model";
import {registry} from "@web/core/registry";
import {standardFieldProps} from "@web/views/fields/standard_field_props";
import {useFileViewer} from "@web/core/file_viewer/file_viewer_hook";

/**
 * A file of the generated e-invoice XML (<Allegati> node), served by
 * /l10n_it_edi_ext/xml_attachment instead of /web/content.
 */
class XmlAttachmentFile extends FileModel {
    /** @type {String} */
    route;

    get urlRoute() {
        return this.route;
    }

    get urlQueryParams() {
        return {};
    }
}

/**
 * Table of the attachments actually present in the generated e-invoice XML.
 * PDF and images open in the file viewer of the chatter, the other files are
 * downloaded.
 */
export class XmlAttachmentsField extends Component {
    static template = "l10n_it_edi_extension.XmlAttachmentsField";
    static props = {...standardFieldProps};

    setup() {
        this.fileViewer = useFileViewer();
    }

    get xmlFiles() {
        return (this.props.record.data[this.props.name] || []).map((data) =>
            Object.assign(new XmlAttachmentFile(), {
                index: data.index,
                name: data.name,
                description: data.description,
                format: data.format,
                size: data.size,
                mimetype: data.mimetype,
                route: data.url,
            })
        );
    }

    formatSize(size) {
        return `${(size / 1024).toFixed(1)} KB`;
    }

    openFile(file, files) {
        this.fileViewer.open(file, files);
    }
}

export const xmlAttachmentsField = {
    component: XmlAttachmentsField,
    supportedTypes: ["json"],
};

registry.category("fields").add("l10n_it_edi_ext_xml_attachments", xmlAttachmentsField);
