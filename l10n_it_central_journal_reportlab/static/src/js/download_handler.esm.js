/** @odoo-module **/

import {registry} from "@web/core/registry";

// Service to handle report download and progress notifications
const reportDownloadService = {
    dependencies: ["bus_service", "notification", "rpc"],

    start(env, {bus_service, notification, rpc}) {
        console.log("=== reportDownloadService started ===");
        let progressNotificationElement = null;
        let notificationCreated = false;
        // Track downloaded attachments to prevent duplicates
        const downloadedAttachments = new Set();

        console.log("Adding bus_service event listener");

        // Helper function to handle download button click
        const handleDownloadClick = async (attachmentId, payload) => {
            // Mark as downloaded when user clicks
            if (attachmentId) {
                downloadedAttachments.add(attachmentId);
                console.log("Added to downloaded set:", attachmentId);
            }

            try {
                // Normalize the URL to the current origin to avoid CORS errors.
                // On odoo.sh, payload.url may contain the internal .dev.odoo.com
                // domain while the browser is on a custom domain (e.g. example.com).
                const parsedUrl = new URL(payload.url);
                const sameOriginUrl =
                    window.location.origin + parsedUrl.pathname + parsedUrl.search;

                // Fetch the entire file into a Blob BEFORE deleting the attachment.
                // This prevents Chrome (and other browsers) from receiving a 404
                // because the server-side file was removed while the download was
                // still in progress.
                console.log("Fetching file as blob...");
                const response = await fetch(sameOriginUrl);
                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}`);
                }
                const blob = await response.blob();
                const blobUrl = URL.createObjectURL(blob);
                console.log("Blob ready, triggering download");

                // Trigger download from the local blob URL (browser-independent)
                const a = document.createElement("a");
                a.href = blobUrl;
                a.setAttribute("download", payload.filename || "report.pdf");
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);

                // Release the blob URL after a short delay
                setTimeout(() => URL.revokeObjectURL(blobUrl), 1000);
                console.log("Download triggered");

                // Close notification now that the blob is in the browser
                const notifElement = document.querySelector(
                    ".o_central_journal_download_ready"
                );
                if (notifElement) {
                    const closeBtn = notifElement.querySelector(
                        ".o_notification_close"
                    );
                    if (closeBtn) {
                        closeBtn.click();
                        console.log("Notification closed after download");
                    }
                }

                // The blob is already in the browser — safe to delete from server now
                if (attachmentId) {
                    rpc("/web/dataset/call_kw", {
                        model: "ir.attachment",
                        method: "unlink",
                        args: [[attachmentId]],
                        kwargs: {},
                    }).catch((error) => {
                        console.warn(
                            "Failed to delete attachment after download:",
                            error
                        );
                    });
                }
            } catch (error) {
                console.error("Download failed:", error);
                // Remove from downloaded set so the user can retry
                if (attachmentId) {
                    downloadedAttachments.delete(attachmentId);
                }
            }
        };

        bus_service.addEventListener("notification", ({detail: notifications}) => {
            console.log("Bus notification received, count:", notifications.length);
            for (const notif of notifications) {
                const {type, payload} = notif;
                console.log("Processing notification type:", type);

                // Handle progress updates
                if (type === "l10n_it_central_journal.report_progress" && payload) {
                    if (!notificationCreated) {
                        // Create initial progress notification only once
                        notification.add(payload.message || "Generating report...", {
                            title: payload.title || "Report Generation",
                            type: "info",
                            sticky: true,
                            className: "o_central_journal_progress",
                        });
                        notificationCreated = true;
                        // Use a small delay to ensure DOM is updated
                        setTimeout(() => {
                            progressNotificationElement = document.querySelector(
                                ".o_central_journal_progress"
                            );
                        }, 100);
                    }

                    // Update progress bar in the notification
                    const notifEl = document.querySelector(
                        ".o_central_journal_progress .o_notification_content"
                    );
                    if (notifEl) {
                        // Remove existing progress bar if any
                        const existingProgress =
                            notifEl.querySelector(".o_progress_bar");
                        if (existingProgress) {
                            existingProgress.remove();
                        }

                        // Add new progress bar
                        const progressHTML = `
                            <div class="o_progress_bar" style="margin-top: 10px;">
                                <div class="progress" style="height: 20px;">
                                    <div class="progress-bar progress-bar-striped progress-bar-animated bg-info"
                                         role="progressbar"
                                         style="width: ${payload.progress || 0}%"
                                         aria-valuenow="${payload.progress || 0}"
                                         aria-valuemin="0"
                                         aria-valuemax="100">
                                        ${payload.progress || 0}%
                                    </div>
                                </div>
                            </div>
                        `;
                        notifEl.insertAdjacentHTML("beforeend", progressHTML);
                    }

                    // Close progress notification when complete
                    if (payload.progress >= 100) {
                        setTimeout(() => {
                            if (progressNotificationElement) {
                                const closeBtn =
                                    progressNotificationElement.querySelector(
                                        ".o_notification_close"
                                    );
                                if (closeBtn) {
                                    closeBtn.click();
                                }
                                progressNotificationElement = null;
                                notificationCreated = false;
                            }
                        }, 1000);
                    }
                }

                // Handle download trigger
                if (type === "l10n_it_central_journal.download_report" && payload) {
                    // Extract attachment ID from URL to check for duplicates
                    const urlParams = new URLSearchParams(new URL(payload.url).search);
                    const attachmentId = parseInt(urlParams.get("id"), 10);

                    console.log(
                        "Download notification received for attachment",
                        attachmentId
                    );
                    console.log("Already downloaded:", downloadedAttachments);

                    // Skip if this attachment was already downloaded
                    if (attachmentId && downloadedAttachments.has(attachmentId)) {
                        console.log(
                            "SKIPPING - Download already triggered for attachment",
                            attachmentId
                        );
                        continue;
                    }

                    // Close progress notification if exists
                    if (progressNotificationElement) {
                        const closeBtn = progressNotificationElement.querySelector(
                            ".o_notification_close"
                        );
                        if (closeBtn) {
                            closeBtn.click();
                        }
                        progressNotificationElement = null;
                        notificationCreated = false;
                    }

                    // Create a STICKY notification with clickable download link
                    notification.add(
                        "Your Central Journal PDF is ready. Click to download.",
                        {
                            title: "✓ Report Ready",
                            type: "success",
                            // CRITICAL: stays until user dismisses
                            sticky: true,
                            className: "o_central_journal_download_ready",
                            buttons: [
                                {
                                    name: "Download PDF",
                                    primary: true,
                                    onClick: () =>
                                        handleDownloadClick(attachmentId, payload),
                                },
                            ],
                        }
                    );
                }
            }
        });
    },
};

registry.category("services").add("reportDownloadService", reportDownloadService);
