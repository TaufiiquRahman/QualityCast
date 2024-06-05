# Display image and classification results
if file is not None:
    # Create two columns for layout
    col1, col2 = st.columns(2)
    
    # Column 1: Image and file name
    with col1:
        image = Image.open(file).convert('RGB')
        st.image(image, use_column_width=True)
        st.markdown(f'<div class="filename-box">Uploaded file: {file.name}</div>', unsafe_allow_html=True)
    
    # Column 2: Classification result and donut chart
    with col2:
        # Classify image
        top_classes = classify(image, model, class_names, top_n=5)
        
        # Calculate percentages for Perfect and Defect
        perfect_percentage = sum([score for class_name, score in top_classes if class_name == "Perfect"]) * 100
        defect_percentage = sum([score for class_name, score in top_classes if class_name == "Defect"]) * 100
        
        # Create a box to display percentage results
        st.markdown(f'<div class="box"><h2>Perfect</h2><h3>Percentage: {perfect_percentage:.1f}%</h3></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="box"><h2>Defect</h2><h3>Percentage: {defect_percentage:.1f}%</h3></div>', unsafe_allow_html=True)
        
        # Create a donut chart for Perfect and Defect predictions
        fig, ax = plt.subplots()
        sizes = [score for class_name, score in top_classes]
        labels = [f'{class_name} ({score*100:.1f}%)' for class_name, score in top_classes]
        colors = ['blue' if class_name == "Perfect" else 'red' for class_name, _ in top_classes]
        ax.pie(sizes, labels=labels, colors=colors, startangle=90, counterclock=False, wedgeprops={'width': 0.3, 'edgecolor': 'w'})
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        st.pyplot(fig)
        
        # Save the result to history
        log = pd.DataFrame([{
            "filename": file.name,
            "class_name": class_name,
            "confidence_score": f"{conf_score*100:.1f}%",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        } for class_name, conf_score in top_classes])
        
        # Load existing history if available
        history_path = os.path.join(os.path.dirname(__file__), 'pages/history.csv')
        try:
            history = pd.read_csv(history_path)
        except FileNotFoundError:
            history = pd.DataFrame(columns=["filename", "class_name", "confidence_score", "timestamp"])
        
        # Append new log using pd.concat
        history = pd.concat([history, log], ignore_index=True)
        
        # Save updated history
        history.to_csv(history_path, index=False)
