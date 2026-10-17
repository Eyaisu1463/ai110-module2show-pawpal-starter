import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

# Initialize the Owner in session state so it survives button clicks
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Pet Owner")
if "scheduler" not in st.session_state:
    st.session_state.scheduler = Scheduler()

owner = st.session_state.owner
scheduler = st.session_state.scheduler

st.title("🐾 PawPal+")
st.markdown("Your smart pet care assistant.")

# ─── Sidebar: Add Pet & Task ───────────────────────────────────────
with st.sidebar:
    st.header("Owner Setup")
    owner.name = st.text_input("Your Name", value=owner.name)
    
    st.divider()
    
    st.header("🐶 Add a Pet")
    with st.form("add_pet_form", clear_on_submit=True):
        pet_name = st.text_input("Pet Name")
        pet_species = st.text_input("Species (e.g., Dog, Cat)")
        pet_breed = st.text_input("Breed")
        pet_age = st.number_input("Age", min_value=0, max_value=30, value=1)
        
        pet_submit = st.form_submit_button("Add Pet")
        if pet_submit:
            if pet_name and pet_species:
                owner.add_pet(Pet(name=pet_name, species=pet_species, breed=pet_breed, age=pet_age))
                st.success(f"Added {pet_name}!")
            else:
                st.error("Name and Species are required.")

    st.divider()

    st.header("📝 Add a Task")
    if not owner.pets:
        st.info("Add a pet first.")
    else:
        with st.form("add_task_form", clear_on_submit=True):
            selected_pet_name = st.selectbox("Assign to Pet", options=[p.name for p in owner.pets])
            task_desc = st.text_input("Task Description (e.g., Morning Walk)")
            task_time = st.text_input("Time (HH:MM)", value="08:00")
            task_freq = st.selectbox("Frequency", options=["daily", "weekly", "once"])
            task_dur = st.number_input("Duration (minutes)", min_value=5, max_value=120, value=30)
            task_priority = st.selectbox("Priority", options=["High", "Medium", "Low"])
            
            task_submit = st.form_submit_button("Add Task")
            if task_submit:
                if task_desc and task_time:
                    # Find the selected pet and add the task
                    target_pet = next(p for p in owner.pets if p.name == selected_pet_name)
                    target_pet.add_task(Task(
                        description=task_desc, time=task_time, frequency=task_freq, 
                        duration_minutes=task_dur, priority=task_priority
                    ))
                    st.success(f"Task added to {selected_pet_name}!")
                else:
                    st.error("Description and Time are required.")

# ─── Main Area: Schedule & Conflicts ───────────────────────────────
st.header(" Today's Schedule")

if not owner.pets:
    st.info("Add a pet and some tasks in the sidebar to see your schedule.")
else:
    # 1. Conflict Warnings
    conflicts = scheduler.detect_conflicts(owner)
    if conflicts:
        for w in conflicts:
            st.warning(w)

    # 2. Sorted Schedule Table
    sorted_tasks = scheduler.sort_by_time(owner)
    
    if not sorted_tasks:
        st.info("No tasks scheduled yet.")
    else:
        # Convert to a list of dicts for st.table
        table_data = []
        for pet_name, task in sorted_tasks:
            table_data.append({
                "Time": task.time,
                "Pet": pet_name,
                "Task": task.description,
                "Status": task.status,
                "Freq": task.frequency,
                "Priority": task.priority
            })
        
        st.table(table_data)

        # 3. Task Completion & Recurrence Demo
        st.divider()
        st.subheader("Mark Task Complete")
        
        # Create a dropdown of tasks to complete
        task_options = {f"{t.time} - {p}: {t.description}": (p, t) for p, t in sorted_tasks if t.status == "pending"}
        
        if task_options:
            selected_task_str = st.selectbox("Select a pending task", options=list(task_options.keys()))
            if st.button("Mark Complete"):
                pet_name, task_obj = task_options[selected_task_str]
                
                # mark_complete returns a new task if it's recurring!
                new_task = task_obj.mark_complete()
                
                if new_task:
                    # Find the pet and add the new occurrence
                    target_pet = next(p for p in owner.pets if p.name == pet_name)
                    target_pet.add_task(new_task)
                    st.success(f"Completed! A new '{new_task.frequency}' task was created for next time.")
                else:
                    st.success("Task completed (no recurrence).")
                
                st.rerun() # Refresh UI to show updated status
        else:
            st.success("All tasks are completed! ")