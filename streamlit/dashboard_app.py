import streamlit as st
from helper_functions import create_connection
from helper_functions import query_table_to_df
import pandas as pd
import plost
import plotly.express as px

# Page setting
# st.set_page_config(layout='wide', initial_sidebar_state='expanded')

# st.title('Students Dashboard')

# with open('style.css') as f:
#     st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# st.sidebar.header('Dashboard Parameters')

def display_dashboard_app(df):
    """Display the main dashboard app."""

    # Sidebar: Select student classes
    class_filter = st.sidebar.multiselect(
        'Select Student Class',
        options=sorted(df['student_class'].unique()),
        key='dashboard_class_filter'
    )

    # Sidebar: Select student statuses
    status_filter = st.sidebar.multiselect(
        'Select Student Status',
        options=sorted(df['student_status'].unique()),
        key='dashboard_status_filter'
    )

    # Apply filters to the DataFrame
    if class_filter:
        df = df[df['student_class'].isin(class_filter)]

    if status_filter:
        df = df[df['student_status'].isin(status_filter)]

    total_students = df['student_id'].nunique()

    # deduplicate the data
    deduplicate_students_by_gender_scores = df.drop_duplicates(subset=['student_id', 'gender', 'student_activity_status'])

    # Aggregate the data by gender
    gender_counts = deduplicate_students_by_gender_scores['gender'].value_counts().reset_index()
    gender_counts.columns = ['gender', 'count']

    # Aggregate the data by assessment student evaluation
    evaluation_counts = deduplicate_students_by_gender_scores['student_activity_status'].value_counts().reset_index()
    evaluation_counts.columns = ['student_activity_status', 'count']

    # Aggregate the data by student offences
    offence_counts = df['student_offence'].value_counts().reset_index()
    offence_counts = offence_counts.sort_values(by='count', ascending=True)
    offence_counts.columns = ['student_offence', 'count']

    # Calculate the attendance rate for each student
    df['student_attendance_rate'] = (df['average_student_minutes_attendance'].astype(int) /
                                    df['average_expected_student_attendance'].astype(int)) * 100

    # Calculate the mean attendance rate
    mean_attendance_rate = df['student_attendance_rate'].mean()

    # Count the number of students who passed SAT
    passed_students = df['sat_performance'].value_counts().get('Pass', 0)

    # Calculate the SAT pass rate as a percentage
    sat_pass_rate = (passed_students / total_students) * 100

    # Create columns for layout
    col1, col2, col3, col4 = st.columns(4)

    # Display the metrics in Streamlit
    col1.metric("Total Students", total_students)
    col2.metric("Average Attendance Rate", f"{mean_attendance_rate:.1f}%")
    col3.metric("Predicted SAT Pass Rate", f"{sat_pass_rate:.1f}%")
    col4.metric("Predicted WAEC Pass Rate", "None")

    # Create three columns with equal width
    col5, col6, col7 = st.columns(3)

    # Donut chart for Gender Ratio
    fig1 = px.pie(
        gender_counts,
        names='gender',
        values='count',
        hole=0.4,
        title='Gender Ratio'
    )
    fig1.update_traces(textposition='inside', textinfo='percent+label',
        hovertemplate='<b>%{label}</b>: %{value}<extra></extra>')
    # Remove legend
    fig1.update_layout(showlegend=False)
    # Display the donut chart
    col5.plotly_chart(fig1, use_container_width=True)


    # Donut chart for Extracurricular Status
    fig1 = px.pie(
        evaluation_counts,
        names='student_activity_status',
        values='count',
        hole=0.4,
        title='Extracurricular Status'
    )
    fig1.update_traces(textposition='inside', textinfo='percent+label',
        hovertemplate='<b>%{label}</b>: %{value}<extra></extra>')
    # Remove legend 
    fig1.update_layout(showlegend=False)
    # Display the donut chart
    col6.plotly_chart(fig1, use_container_width=True)


    # Bar chart for Student Offences
    fig1 = px.bar(
        offence_counts,
        x='count',
        y='student_offence',
        orientation='h',
        title='Student Offences'
    )
    fig1.update_traces(
        texttemplate='%{x}',
        textposition='inside',
        hovertemplate='<b>%{y}</b>: %{x}<extra></extra>'
    )
    # Remove y-axis title
    fig1.update_layout(yaxis_title=None)
    # Display the bar chart
    col7.plotly_chart(fig1, use_container_width=True)