"""
Analysis page for the Dental AI application
Handles patient information input, image upload, and analysis functions
"""
import streamlit as st
from typing import Dict, Any, List
import io
from PIL import Image
from datetime import datetime

def render_analysis_page():
    """Render the patient analysis page"""
    st.header("Patient Analysis")
    
    # Check if API key is set
    if not st.session_state.get("api_key"):
        st.info("Please enter your OpenAI API key in the sidebar to continue.")
        return
    
    # Initialize components if needed
    ai_engine = st.session_state.ai_engine
    report_generator = st.session_state.report_generator
    image_processor = st.session_state.image_processor
    
    if not ai_engine or not report_generator or not image_processor:
        st.error("Failed to initialize AI components. Please check your API key.")
        return
    
    # Patient information form
    st.subheader("Patient Information")
    
    col1, col2 = st.columns(2)
    with col1:
        patient_name = st.text_input("Patient Name")
        patient_age = st.number_input("Age", min_value=0, max_value=120, value=30)
        patient_gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    
    with col2:
        patient_complaint = st.text_area("Primary Complaint")
        patient_history = st.text_area("Medical History")
    
    # Image upload section
    st.subheader("Dental Images")
    st.write("Upload dental X-rays or intraoral photos for analysis.")
    
    uploaded_files = st.file_uploader(
        "Upload dental images", 
        type=["jpg", "jpeg", "png"], 
        accept_multiple_files=True
    )
    
    # Display uploaded images
    images = []
    if uploaded_files:
        st.write(f"{len(uploaded_files)} images uploaded")
        
        # Create columns for image display
        num_cols = min(3, len(uploaded_files))
        cols = st.columns(num_cols)
        
        for i, file in enumerate(uploaded_files):
            img = Image.open(file)
            images.append(img)
            cols[i % num_cols].image(img, caption=f"Image {i+1}", use_column_width=True)
    
    # Analysis button
    if st.button("Analyze Images"):
        if not images:
            st.error("Please upload at least one dental image for analysis.")
            return
            
        if not patient_name:
            st.error("Please enter patient name.")
            return
        
        # Collect patient information
        patient_info = {
            "name": patient_name,
            "age": patient_age,
            "gender": patient_gender,
            "complaint": patient_complaint,
            "medical_history": patient_history,
        }
        
        # Process images
        with st.spinner("Processing images..."):
            processed_images = image_processor.process_batch(images)
        
        # Analyze images
        with st.spinner("Analyzing dental images..."):
            try:
                # Get AI analysis
                analysis = ai_engine.analyze_images(processed_images, patient_info)
                
                # Generate reports
                detailed_report = report_generator.generate_detailed_report(analysis, patient_info)
                summary_report = report_generator.generate_summary_report(analysis, patient_info)
                
                # Store results
                results = {
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "patient_info": patient_info,
                    "raw_analysis": analysis,
                    "detailed_report": detailed_report,
                    "summary_report": summary_report
                }
                
                st.session_state.current_analysis = results
                
                # Save to history
                if 'history' not in st.session_state:
                    st.session_state.history = []
                
                st.session_state.history.append({
                    "timestamp": results["timestamp"],
                    "patient": patient_name,
                    "results": results
                })
                
                # Show success message
                st.success("Analysis complete!")
                
                # Display results
                display_analysis_results(results)
                
            except Exception as e:
                st.error(f"Error during analysis: {str(e)}")
                

def display_analysis_results(results: Dict[str, Any]):
    """Display analysis results"""
    # Summary report (for doctor's signature)
    st.subheader("Summary Report")
    st.info("This is the concise report for the doctor to review and sign.")
    st.markdown(results["summary_report"])
    
    # Download options
    col1, col2 = st.columns(2)
    with col1:
        summary_bytes = results["summary_report"].encode("utf-8")
        st.download_button(
            label="Download Summary Report (PDF)",
            data=summary_bytes,
            file_name=f"dental_summary_{results['timestamp'].replace(':', '-').replace(' ', '_')}.txt",
            mime="text/plain"
        )
    
    # Detailed report
    st.subheader("Detailed Report")
    st.info("This report explains the reasoning behind the analysis in detail.")
    with st.expander("View Detailed Report"):
        st.markdown(results["detailed_report"])
    
    # Download detailed report
    with col2:
        detailed_bytes = results["detailed_report"].encode("utf-8")
        st.download_button(
            label="Download Detailed Report (PDF)",
            data=detailed_bytes,
            file_name=f"dental_detailed_{results['timestamp'].replace(':', '-').replace(' ', '_')}.txt",
            mime="text/plain"
        )
    
    # CRM export option
    if st.session_state.crm_settings["type"] != "None":
        st.button("Export to CRM", key="export_to_crm")