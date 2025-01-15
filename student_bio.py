import streamlit as st
from helper_functions import create_connection
from helper_functions import query_table_to_df
import pandas as pd
import plotly.graph_objects as go


def display_student_bio(df):
    """Display the Student Bio app."""

    # Sidebar: Select student classes
    class_filter = st.sidebar.selectbox(
        'Select Student Class',
        options=sorted(df['student_class'].dropna().unique()),
        key='bio_student_class_filter'
    )

    # Filter the DataFrame based on the selected class to update name options
    if class_filter:
        filtered_df = df[df['student_class'] == class_filter]
    else:
        filtered_df = df  # If no class is selected, show all names

    # Sidebar: Select student names (filtered by the selected class)
    name_filter = st.sidebar.selectbox(
        'Select Student Name',
        options=sorted(filtered_df['student_name'].dropna().unique()),
        key='bio_name_filter'
    )

    # Apply final filters to the DataFrame
    if class_filter:
        df = df[df['student_class'] == class_filter]

    if name_filter:
        df = df[df['student_name'] == name_filter]

    # Sidebar: Select student class (Specific to the Attendance of the student)
    attendance_class_filter = st.sidebar.selectbox(
        'Select Student Attendance Class',
        options=sorted(filtered_df['course_class'].dropna().unique()),
        key='bio_attendance_class_filter'
    )

    # Apply final filters to the DataFrame
    if class_filter:
        df = df[df['student_class'] == class_filter]

    if name_filter:
        df = df[df['student_name'] == name_filter]

    if attendance_class_filter:
        df1 = df[df['course_class'] == attendance_class_filter]

    if df["gender"].iloc[0] == 'Male':
        # CSS for the banner
        banner_style = """
        <style>
        .banner-container {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 150px; /* Adjust height as needed */
            background-color: #6663ff; /* Light purple background */
            border-radius: 20px 20px 20px 20px; /* Curved edges */
            z-index: 0; /* Ensure it stays behind the content but above the page background */
        }
        .content-container {
            position: relative; /* Keeps content on top */
            z-index: 1; /* Ensures content appears above the banner */
            padding-top: 30px; /* Add padding to prevent overlap with the banner */
        }
        .image-container {
            margin-left: 200px; /* Adjust this value to shift the image to the right */
        }
        </style>
        """

    else:
        # CSS for the banner
        banner_style = """
        <style>
        .banner-container {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 150px; /* Adjust height as needed */
            background-color: #c062e0; /* Light purple background */
            border-radius: 20px 20px 20px 20px; /* Curved edges */
            z-index: 0; /* Ensure it stays behind the content but above the page background */
        }
        .content-container {
            position: relative; /* Keeps content on top */
            z-index: 1; /* Ensures content appears above the banner */
            padding-top: 30px; /* Add padding to prevent overlap with the banner */
        }
        .image-container {
            margin-left: 200px; /* Adjust this value to shift the image to the right */
        }
        </style>
        """

    # Add the CSS to the page
    st.markdown(banner_style, unsafe_allow_html=True)

    # Add the banner div
    st.markdown('<div class="banner-container"></div>', unsafe_allow_html=True)

    # Display profile image if the filtered DataFrame is not empty
    profile_image = f"./images/{df['profile_image'].iloc[0]}"

    # Create two columns: one for the image, one for other content
    col1, col2, col3 = st.columns([1.5, 4, 2])

    # Display image in the first column with a specific width
    with col1:
        st.markdown('<div class="image-container">', unsafe_allow_html=True)
        st.image(profile_image, use_container_width=True)  # Width will be adjusted, height will scale
        st.markdown('</div>', unsafe_allow_html=True)

    # Content for col2 (two rows)
    with col2:
        # Add empty text to push text down
        with st.container():
            st.markdown("<br>" * 2, unsafe_allow_html=True)

        # Combine name and class with no gap
        with st.container():
            st.markdown(
                f"""
                <p style="margin: 0; color: white; font-weight: bold;">{df['student_name'].iloc[0]}</p>
                <p style="margin: 0; color: white; ">{df['student_class'].iloc[0]}</p>
                """,
                unsafe_allow_html=True
            )

    with col3:
        # Add empty text to push text down
        with st.container():
            st.markdown("<br>" * 2, unsafe_allow_html=True)

        with st.container():
        # Display a key icon using emoji
            st.write(f"**🔑 <span style='color: white;'>{df['student_id'].iloc[0]}</span>**", unsafe_allow_html=True)
            

    # Add Text Metrics
    st.markdown(
    """
    <style>
    [data-testid="stMetricValue"] {
        font-size: 18px;
        font-weight: 550; /* Lighter bold */
    }
    </style>
    """,
    unsafe_allow_html=True,
    )

    row1, row2, row3 = st.columns(3)
    row1.metric("First Name", df['student_name'].iloc[0].split()[0])
    row2.metric("Gender", df['gender'].iloc[0])
    row3.metric("Bus Pickup?", df['bus_pickup'].iloc[0])


    row4, row5, row6 = st.columns(3)
    row4.metric("Last Name", df['student_name'].iloc[0].split()[-1])
    row5.metric("Student ID", df['student_id'].iloc[0])
    row6.metric("Bus Dropoff?", df['bus_dropoff'].iloc[0])


    row7, row8, row9 = st.columns(3)
    row7.metric("Preferred Name", df['student_name'].iloc[0].split()[0])
    row8.metric("Student Status", df['student_status'].iloc[0])
    row9.metric("Health Condition", df['health_condition'].iloc[0])


    row10, row11, row12 = st.columns(3)
    row10.metric("Parent Name", " ".join(df['parent'].iloc[0].split()[1:]))
    row11.metric("Extracurricular Activity", df['student_extracurricular_activity'].iloc[0])
    row12.metric("Offence", df['student_offence'].iloc[0])

    # Add Horizontal line
    st.markdown(
    """
    <hr style="border: 1px solid #d3aef5;"/>
    """, 
    unsafe_allow_html=True
    )

    # deduplicate the data
    attendance_df = df1.drop_duplicates(subset=['student_id', 'course', 'average_student_minutes_attendance', 'average_expected_student_attendance'])

    # Calculate the attendance rate for each student course
    attendance_df['student_attendance_rate'] = (attendance_df['average_student_minutes_attendance'].astype(int) /
                                    attendance_df['average_expected_student_attendance'].astype(int)) * 100

    df1 = attendance_df.groupby('course', as_index=False)['student_attendance_rate'].mean().round({'student_attendance_rate': 1})

    st.subheader("Student Course Attendance")

    if not df1.empty:

        col1, col2 = st.columns(2)

        # Sample Data
        df_left = df1.iloc[:len(df1)//2] 
        df_right = df1.iloc[len(df1)//2:]

        # Create figure with subplots for side-by-side "curvy" bars
        fig = go.Figure()
        fig1 = go.Figure()

        # Left group bars as "curvy"
        fig.add_trace(go.Scatter(
            y=df_left['course'],
            x=df_left['student_attendance_rate'],
            mode='markers+lines',
            marker=dict(
                size=15,
                color=df_left['student_attendance_rate'], 
                colorscale='Viridis',
                line=dict(width=2, color='rgba(0,0,0,0.5)'),
                symbol='circle',  # Circular marker for curvy effect
            ),
            line=dict(width=4, shape='spline'),  # Curvy lines (spline) for smooth effect
            name='Left Group',
            showlegend=False
        ))

        # Right group bars as "curvy"
        fig1.add_trace(go.Scatter(
            y=df_right['course'],
            x=df_right['student_attendance_rate'],
            mode='markers+lines',
            marker=dict(
                size=15,
                color=df_right['student_attendance_rate'], 
                colorscale='Plasma',
                line=dict(width=2, color='rgba(0,0,0,0.5)'),
                symbol='circle',  # Circular marker for curvy effect
            ),
            line=dict(width=4, shape='spline'),  # Curvy lines (spline) for smooth effect
            name='Right Group',
            showlegend=False
        ))

        # Update layout to position charts side by side and set x-axis range
        fig.update_layout(
            title='',
            barmode='stack',  # Use stack mode for better visualization of the curves
            xaxis=dict(
                title=None,
                range=[0, 100]  # Set x-axis range from 0 to 100
            ),
            yaxis=None,
            margin=dict(l=50, r=50, t=50, b=50),
            plot_bgcolor='white',
            paper_bgcolor='white',
            showlegend=True
        )

        # Update layout to position charts side by side and set x-axis range
        fig1.update_layout(
            title='',
            barmode='stack',  # Use stack mode for better visualization of the curves
            xaxis=dict(
                title=None,
                range=[0, 100]  # Set x-axis range from 0 to 100
            ),
            yaxis=None,
            margin=dict(l=50, r=50, t=50, b=50),
            plot_bgcolor='white',
            paper_bgcolor='white',
            showlegend=True
        )

        # Display charts in the columns
        col1.plotly_chart(fig, use_container_width=True, key="left_col_chart")
        col2.plotly_chart(fig1, use_container_width=True, key="right_col_chart")
    
    else:
        st.markdown("<span style='font-size:20px; '>This student don't have any active course</span>", unsafe_allow_html=True)