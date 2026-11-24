# Recover a completed export handoff

1. Read the final project verification report and delivery receipt before retrying work, because an intermediate child handoff can predate successful parent mastering. Compare the final filename, stream expectations, validation status and recorded delivery separately from the child's picture-only result.

2. Check the exact final artifact with a read-only file lookup, because a successful historical report does not establish current file presence. On Windows use `Get-Item -LiteralPath "C:/absolute/project/final-v001.mp4" | Select-Object FullName,Length`; when invoking through JavaScript, keep forward slashes in this command string or escape backslashes deliberately so the lookup addresses the intended file. Probe audio only if the final report does not establish the expected audio-bearing artifact.

3. Preserve a verified completed export when only its completion notification failed, because repeating a render or mux can overwrite evidence without fixing delivery. State that export verification passed and notification delivery failed only when both states have supporting evidence. Treat viewing or playback on the recipient's side as unverified until confirmed.

4. Send the verified final through the current surface's native media attachment when delivery remains outstanding, because a prose path alone does not supply playable media. Put its exact absolute saved path in the same completion caption. Inspect the send result for attachment name, MIME type and delivery status before recording it as sent; distinguish tool-confirmed sending from recipient-confirmed playback.

5. Answer a request for the path with the checked final audio-bearing file's absolute path, because the user is asking for the saved artifact rather than another production attempt. Label it briefly as the full film with audio when silent intermediates exist, and omit unrelated memory or runtime diagnostics from that lookup response.

6. Reconcile later intermediate completion events against the final report before updating the progress card or notifying the user, because repeated child reports must not reopen completed mastering or duplicate a delivered update. Keep production, delivery and viewer-review states separate; leave stopped or idle work untouched on a status-only request.
