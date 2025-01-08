# Libraries and Modules
import streamlit as st

# Tutorial Steps
def get_tutorial_steps():
    """
    Returns a list of tutorial steps for accident reporting.
    """
    return [
        "First determine if anyone is injured.",
        "Ask for the basic vehicle information before taking a statement from the driver.",
        "Once a statement is obtained, determine if this is an accident or an incident.",
        "Ask for pictures of all vehicles involved from all four sides from a wide angle.",
        "Obtain other motorists' contact and insurance information.",
        "If police are involved, determine if a citation has been issued.",
        "If a citation has been issued, proceed with the post-accident testing SOP.",
        "If any injuries are sustained, determine if EMS will transport anyone from the scene. If so, where are they being transported?",
        "If a tow is required, determine if the vehicle is disabled. If it is being towed, obtain the tow company information.",
    ]

# Tutorial Function
def tutorial():
    """
    Provides a step-by-step accident reporting tutorial.
    """
    st.title("Accident Reporting SOP Tutorial")
    # Initialize session state for the current step
    if "current_step" not in st.session_state:
        st.session_state.current_step = 0
    # Retrieve tutorial steps
    steps = get_tutorial_steps()
    # Show progress bar
    progress = (st.session_state.current_step + 1) / len(steps)
    st.progress(progress)
    # Display the current step
    if st.session_state.current_step < len(steps):
        step = steps[st.session_state.current_step]
        st.markdown(f"**Step {st.session_state.current_step + 1}: {step}**")
        # Navigation buttons
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("Previous", key="previous_step", disabled=st.session_state.current_step == 0):
                st.session_state.current_step -= 1
        with col2:
            if st.button("Next", key="next_step"):
                st.session_state.current_step += 1
    else:
        st.success("Tutorial Complete!")
        if st.button("Restart Tutorial"):
            st.session_state.current_step = 0