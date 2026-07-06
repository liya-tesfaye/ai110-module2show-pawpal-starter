from datetime import time

import streamlit as st

from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown("A pet care planning assistant. Add your pets and their care tasks below.")

with st.expander("Scenario", expanded=False):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.
"""
    )

# --- Persist a single Owner across reruns -----------------------------------
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan")

owner = st.session_state.owner

# Priority is stored as an int on Task (1 = high, 2 = medium, 3 = low); the form
# shows friendly labels and maps them back to those ints.
PRIORITY_TO_INT = {"high": 1, "medium": 2, "low": 3}
INT_TO_PRIORITY = {1: "high", 2: "medium", 3: "low"}

st.divider()

# --- Add a pet ---------------------------------------------------------------
st.subheader("Add a Pet")

with st.form("add_pet_form", clear_on_submit=True):
    name = st.text_input("Name")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    breed = st.text_input("Breed")
    age = st.number_input("Age (years)", min_value=0, max_value=50, value=1, step=1)
    pet_submitted = st.form_submit_button("Add pet")

    if pet_submitted:
        if not name.strip():
            st.error("Please enter a pet name.")
        else:
            pet = Pet(name=name.strip(), species=species, breed=breed, age=int(age), notes="")
            owner.add_pet(pet)
            st.success(f"Added {pet.name}!")

# Show the current pets so the user can confirm the add worked.
if owner.pets:
    st.write("**Your pets:**")
    for pet in owner.pets:
        st.write(f"- {pet.name} ({pet.species})")
else:
    st.info("No pets yet. Add one above.")

st.divider()

# --- Add a task --------------------------------------------------------------
st.subheader("Add a Task")

if not owner.pets:
    st.info("Add a pet first — tasks belong to a pet.")
else:
    with st.form("add_task_form", clear_on_submit=True):
        description = st.text_input("Description")
        pet_name = st.selectbox("Pet", [pet.name for pet in owner.pets])
        preferred_time = st.time_input("Preferred time", value=time(8, 0))
        priority_label = st.selectbox("Priority", ["high", "medium", "low"])
        duration = st.number_input(
            "Duration (minutes)", min_value=1, max_value=240, value=20, step=1
        )
        task_submitted = st.form_submit_button("Add task")

        if task_submitted:
            if not description.strip():
                st.error("Please enter a task description.")
            else:
                task = Task(
                    name=description.strip(),
                    pet_name=pet_name,
                    duration=int(duration),
                    priority=PRIORITY_TO_INT[priority_label],
                    category="general",
                    preferred_time=preferred_time,
                    recurrence="daily",
                    completed=False,
                )
                # Tasks live on the Pet, so add to the selected pet.
                owner.get_pet(pet_name).add_task(task)
                st.success(f"Added {task.name} for {pet_name}!")

# Show the combined task list across all pets.
all_tasks = owner.get_all_tasks()
if all_tasks:
    st.write("**Current tasks:**")
    for task in all_tasks:
        clock = task.preferred_time.strftime("%H:%M")
        st.write(
            f"- {clock} — {task.name} ({task.pet_name}) "
            f"[{task.duration} min, priority: {INT_TO_PRIORITY[task.priority]}]"
        )
elif owner.pets:
    st.info("No tasks yet. Add one above.")
