import streamlit as st
from helper_functions import create_connection
from helper_functions import query_table_to_df
import pandas as pd
import plotly.graph_objects as go
import re


def display_student_performance(df, df2):
    """Display the Student Performance app."""

    # Sidebar: Select student classes
    class_filter = st.sidebar.selectbox(
        'Select Student Class',
        options=sorted(df['student_class'].dropna().unique()),
        key='performance_student_class_filter'
    )

    # Filter the DataFrame based on the selected class to update name options
    if class_filter:
        filtered_df = df[df['student_class'] == class_filter]
        filtered_df2 = df2[df2['student_class'] == class_filter]
    else:
        filtered_df2 = df2  # If no class is selected, show all names

    # Sidebar: Select student names (filtered by the selected class)
    name_filter = st.sidebar.selectbox(
        'Select Student Name',
        options=sorted(filtered_df['student_name'].dropna().unique()),
        key='performance_name_filter'
    )

    # Apply final filters to the DataFrame
    if class_filter:
        df = df[df['student_class'] == class_filter]
        df2 = df2[df2['student_class'] == class_filter]

    if name_filter:
        df = df[df['student_name'] == name_filter]
        df2 = df2[df2['student_name'] == name_filter]

    # Sidebar: Select student class (Specific to the Performance of the student)
    performance_class_filter = st.sidebar.selectbox(
        'Select Student Desired Academic Class',
        options=sorted(filtered_df['course_class'].dropna().unique()),
        key='performance_class_filter'
    )

    # Apply final filters to the DataFrame
    if class_filter:
        df = df[df['student_class'] == class_filter]

    if name_filter:
        df = df[df['student_name'] == name_filter]

    if performance_class_filter:
        df1 = df[df['course_class'] == performance_class_filter]

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


    # Add Horizontal line
    st.markdown(
    """
    <hr style="border: 1px solid #d3aef5;"/>
    """, 
    unsafe_allow_html=True
    )

    # deduplicate the data
    performance_df = df1.drop_duplicates(subset=['student_id', 'course', 'average_student_score'])

    df1 = performance_df.groupby('course', as_index=False)['average_student_score'].mean().round({'average_student_score': 1})

    st.subheader("Academic Performance")

    col1, col2 = st.columns(2)

    if not df1.empty:

            # Assign colors based on score
        def assign_color(score):
            if score < 50:
                return f'rgba(255, {int(255 * (score / 50))}, 0, 1)'  # Shades of orange
            elif score == 50:
                return 'rgba(255, 255, 0, 1)'  # Yellow
            else:
                return f'rgba({int(255 * ((100 - score) / 50))}, 255, 0, 1)'  # Shades of green

        # Apply the function to create a list of colors
        colors = df1['average_student_score'].apply(assign_color)

        # Create figure with subplots for side-by-side "curvy" bars
        fig = go.Figure()

        # Left group bars as "curvy"
        fig.add_trace(go.Scatter(
            y=df1['course'],
            x=df1['average_student_score'],
            mode='markers',
            marker=dict(
                size=15,
                color=colors, 
                colorscale='Viridis',
                line=dict(width=2, color='rgba(0,0,0,0.5)'),
                symbol='circle',  # Circular marker for curvy effect
            ),
            line=dict(width=4, shape='spline'),  # Curvy lines (spline) for smooth effect
            name='Left Group',
            showlegend=False
        ))

        # Update layout to position charts side by side and set x-axis range
        fig.update_layout(
            title='Internal Exams',
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
    
    else:
        st.markdown("<span style='font-size:20px; '>This student don't have any active course</span>", unsafe_allow_html=True)


    student_class = df['student_class'].iloc[0]

    with col2:
        st.markdown("<span style='font-size:18px; font-weight:bold;'>External Exams</span>", unsafe_allow_html=True)
        with st.container():
            if student_class.startswith('Junior'):
                col2.markdown("<span style='font-size:20px; '>This student needs to be in Senior Secondary School to have external exams predictions</span>", unsafe_allow_html=True)

            elif student_class.startswith('Senior'):
                # Display Predicted SAT score
                predicted_sat_score = df2['Predicted SAT Score'].iloc[0].astype(int)
                col2.markdown(f"<span style='font-size:20px;'>Predicted SAT score: {predicted_sat_score:.0f}</span>", unsafe_allow_html=True)

            elif student_class.startswith('Alumni'):
                # Display SAT score
                sat_score = df2['sat_score'].iloc[0]
                col2.markdown(f'<span style="font-size:20px;">SAT score: {sat_score}</span>', unsafe_allow_html=True)

        with st.container():
            if student_class.startswith('Senior'):
                col2.markdown("<span style='font-size:20px; '>Incoming Predictions</span>", unsafe_allow_html=True)

            elif student_class.startswith('Alumni'):
                # Filter for courses and grades from the maximum year between 2019 and 2021
                df['waec_exam_year'] = df['waec_exam_year'].astype(int)
                max_year = df[df['waec_exam_year'].between(2019, 2021)]['waec_exam_year'].max()

                # Deduplicate the data and filter by the maximum year in the specified range
                df = df.drop_duplicates(subset=['waec_course', 'waec_grade'])
                df = df[df['waec_exam_year'] == max_year]

                # Assign only the relevant columns
                df = df[['waec_course', 'waec_grade']]

                # Define grade to value mapping
                grade_to_value = {
                    'A1': 1.0, 'B2': 0.9, 'B3': 0.8,
                    'C4': 0.7, 'C5': 0.6, 'C6': 0.5,
                    'D7': 0.4, 'E8': 0.3, 'F9': 0.2
                }
                df['value'] = df['waec_grade'].map(grade_to_value)

                # Define color shades
                color_map = {
                    'A1': '#0070C0', 'B2': '#00A2E8', 'B3': '#7FDBFF',
                    'C4': '#FFDC00', 'C5': '#FFD700', 'C6': '#FFBF00',
                    'D7': '#FFBF00', 'E8': '#FFA500', 'F9': '#FF4500'
                }
                df['color'] = df['waec_grade'].map(color_map)

                # Create the figure with "curvy" bars
                fig = go.Figure()

                # Add lollipop markers for each course
                for i, row in df.iterrows():
                    fig.add_trace(go.Scatter(
                        y=[row['waec_course']], 
                        x=[row['value']], 
                        mode='markers+text',
                        marker=dict(
                            size=15, 
                            color=row['color'], 
                            line=dict(width=2, color='rgba(0,0,0,0.5)'),
                            symbol='circle'
                        ),
                        text=row['waec_grade'],
                        textposition='middle right',
                        line=dict(width=4, shape='spline'),
                        name=row['waec_course'],
                        showlegend=False
                    ))

                # Add horizontal lines for the bars
                for i, row in df.iterrows():
                    fig.add_trace(go.Scatter(
                        y=[row['waec_course'], row['waec_course']],
                        x=[0, row['value']],
                        mode='lines',
                        line=dict(color=row['color'], width=2, shape='spline'),
                        showlegend=False
                    ))

                # Update layout
                fig.update_layout(
                    title='WAEC Grades',
                    barmode='stack',
                    xaxis=dict(
                        title=None,
                        range=[0, 1.2],  # Set x-axis range from 0 to slightly beyond 1.0 for padding
                        showgrid=False,
                        zeroline=False,
                        visible=False
                    ),
                    yaxis=dict(
                        title=None,
                        showgrid=False,
                    ),
                    margin=dict(l=50, r=50, t=50, b=50),
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    showlegend=False
                )

                col2.plotly_chart(fig, use_container_width=True)


    if student_class.startswith('Senior'):
        # Add the recommendations section
        col3, col4 = st.columns(2)

        # Subheader for the SAT recommendations section
        col3.subheader("SAT Recommendations")

        sat_recommendations = df2["Recommendation"].iloc[0]

        if pd.isna(sat_recommendations):
            sat_recommendations = ""  
        else:
            sat_recommendations = str(sat_recommendations)

        # Strip any leading/trailing spaces from the whole string
        sat_recommendations = sat_recommendations.strip()

        # Split by '.' or '!' and remove any empty strings
        sat_recommendations = [phrase.strip() for phrase in re.split(r'[.!]', sat_recommendations) if phrase.strip()]

        # Join with newline characters
        sat_recommendations = "\n".join([f"- {phrase}" for phrase in sat_recommendations])

        # Display the recommendations in markdown
        col3.markdown(sat_recommendations, unsafe_allow_html=True)