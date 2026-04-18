from __future__ import annotations

import streamlit as st

try:
    from .extractor import ExtractionError, extract_email
    from .schemas import EmailExtraction
    from .storage import load_events, save_event
except ImportError:
    from extractor import ExtractionError, extract_email
    from schemas import EmailExtraction
    from storage import load_events, save_event


def build_summary(result: EmailExtraction) -> str:
    event_count = len(result.events)
    action_count = sum(1 for event in result.events if event.action_required is True)
    school_name = result.school_name or "the school email"

    if event_count == 0:
        return f"No events or parent actions were found in {school_name}."

    event_label = "event" if event_count == 1 else "events"
    action_label = "action" if action_count == 1 else "actions"
    return (
        f"Found {event_count} {event_label} in {school_name}. "
        f"{action_count} parent {action_label} appear to be required."
    )


def render_event(event_index: int, event: dict) -> None:
    title = event.get("title") or f"Event {event_index}"
    subtype = event.get("event_type") or "Unspecified type"
    with st.container(border=True):
        st.subheader(title)
        st.caption(subtype)

        left, right = st.columns(2)
        with left:
            st.write("**Date:**", event.get("date") or "Unknown")
            st.write("**Start time:**", event.get("start_time") or "Unknown")
            st.write("**End time:**", event.get("end_time") or "Unknown")
            st.write("**Location:**", event.get("location") or "Unknown")
            st.write("**Deadline:**", event.get("deadline") or "Unknown")
        with right:
            st.write("**Child specific:**", event.get("child_specific"))
            st.write("**Action required:**", event.get("action_required"))
            st.write("**Cost:**", event.get("cost") or "Unknown")
            st.write("**Confidence:**", event.get("confidence"))
            items_needed = event.get("items_needed")
            st.write("**Items needed:**", ", ".join(items_needed) if items_needed else "None stated")


def render_saved_events() -> None:
    st.markdown("### All extracted events")

    events = load_events()

    if not events:
        st.info("No stored events yet.")
    else:
        for i, e in enumerate(events, start=1):
            with st.expander(f"Saved email {i}"):
                st.json(e)


def main() -> None:
    st.set_page_config(
        page_title="School Email Event Extractor",
        page_icon="📚",
        layout="wide",
    )

    st.title("School Email Event Extractor")
    st.write("Paste a school email to extract events, deadlines, and parent actions.")

    with st.form("extract_form"):
        email_subject = st.text_input("Email subject")
        email_body = st.text_area("Email body", height=260)
        submitted = st.form_submit_button("Extract events", use_container_width=True)

    if not submitted:
        render_saved_events()
        return

    if not email_body.strip():
        st.warning("Enter the email body before extracting.")
        render_saved_events()
        return

    with st.spinner("Extracting events..."):
        try:
            result = extract_email(email_subject=email_subject, email_body=email_body)
            save_event(result.model_dump())
        except ExtractionError as exc:
            st.error(str(exc))
            return
        except Exception as exc:
            st.error(f"Unexpected error: {exc}")
            return

    st.success("Extraction complete.")
    st.markdown("### Summary")
    st.write(build_summary(result))

    st.markdown("### Structured events")
    if not result.events:
        st.info("No structured events were extracted.")
    else:
        for index, event in enumerate(result.model_dump()["events"], start=1):
            render_event(index, event)

    with st.expander("View JSON"):
        st.json(result.model_dump(mode="json"), expanded=True)

    render_saved_events()


if __name__ == "__main__":
    main()
