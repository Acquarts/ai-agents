# 🎨 Miniature Painter AI Assistant

AI-powered multi-agent system that helps you plan and visualize your miniature painting projects with color schemes, time estimates, and budget calculations.

## ✨ What does it do?

Upload a photo of your unpainted miniature and get:

- **Color Scheme Suggestions**: 3 creative color schemes with specific paint recommendations (Citadel, Vallejo, Army Painter)
- **Time Estimation**: Painting time estimates for Beginner, Intermediate, and Advanced skill levels
- **Budget Calculator**: Complete paint budget breakdown including base colors, shades, highlights, and special effects
- **AI-Generated Painted Renders**: Real photorealistic renders of your miniature painted with each color scheme using Imagen 3

## 🤖 How does it work?

The system uses four specialized AI agents working together:

1. **ColorSchemeAgent**: Analyzes your miniature and suggests creative color schemes based on type, theme, and current painting trends
2. **EstimatorAgent**: Calculates painting time and budget based on miniature complexity and detail level
3. **ImagePainterAgent**: Creates detailed visualization descriptions of the painted result
4. **MiniaturePainterAgent** (root): Coordinates all agents ensuring proper workflow

Each agent has access to Google Search to provide up-to-date paint recommendations and prices.

## 🚀 Quick Start

### Requirements

- Python 3.10 or higher
- Google ADK (Agent Development Kit)
- Streamlit
- Pillow (PIL)
- Google AI API Key ([Get one free here](https://aistudio.google.com/app/apikey))

### Installation

1. **Clone or download this project**

2. **Install dependencies:**
```bash
cd miniature_painter_agent
pip install -r requirements.txt
```

3. **Set up your API key** (Optional - you can also enter it in the UI):
```bash
cp .env.example .env
# Edit .env and add your Google API key
```

### Running the App

1. **Start the Streamlit application:**
```bash
streamlit run agent.py
```

2. **Open your browser** to `http://localhost:8501`

3. **Enter your Google API Key** in the sidebar Configuration section

4. **Upload a miniature image** and click "Analyze Miniature"

## 📸 Photography Tips for Best Results

- **Lighting**: Use natural light or a well-lit workspace
- **Background**: Use a neutral background (white, grey, or black)
- **Focus**: Ensure the miniature is sharp and in focus
- **Framing**: Include the entire miniature in the photo
- **Preparation**: Clean mold lines and prime if possible for better analysis

## 🎯 Use Cases

- **Planning New Projects**: Get color ideas before buying paints
- **Budget Planning**: Know exactly what paints you need and their cost
- **Time Management**: Estimate how long a project will take
- **Skill Development**: Get painting technique recommendations
- **Collection Planning**: Coordinate color schemes across multiple miniatures

## 📋 Example Workflow

1. Upload photo of unpainted Space Marine miniature
2. AI suggests 3 color schemes:
   - Ultramarine Blue with Gold accents
   - Blood Angels Red with Black details
   - Custom Dark Green with Bronze
3. Get time estimate: Beginner (8-12 hours), Advanced (4-6 hours)
4. See budget breakdown: $25-35 for complete paint set
5. **Generate AI Renders**: Click buttons to generate photorealistic painted versions with each color scheme using Google Imagen 3

## 🏗️ Architecture

```
MiniaturePainterAgent (root)
    ├── ColorSchemeAgent (suggests 3 color schemes)
    ├── EstimatorAgent (calculates time & budget)
    └── ImagePainterAgent (visualizes painted result)
```

The root agent coordinates the workflow, ensuring each request flows through color analysis, estimation, and visualization before delivering comprehensive results.

## 🛠️ Technical Details

- **Analysis Model**: Google Gemini 2.5 Flash (multimodal)
- **Image Generation**: Google Imagen 3 (generate-001)
- **Framework**: Google ADK (Agent Development Kit)
- **UI Framework**: Streamlit
- **Image Processing**: Pillow (PIL)
- **Search Integration**: Google Search via google-adk

## 💡 Tips

### For Beginners
- Start with simpler color schemes (2-3 colors)
- Follow the base-shade-highlight approach suggested
- Use the time estimates to plan your first projects

### For Intermediate Painters
- Experiment with the suggested color combinations
- Try different techniques mentioned in the visualization
- Use budget estimates to try new paint brands

### For Advanced Painters
- Use color schemes as starting points for custom variations
- Reference the technique suggestions for complex effects
- Coordinate color schemes across army collections

## 🔧 Troubleshooting

**"Error analyzing miniature"**
- Check that your Google API Key is valid
- Ensure you have internet connectivity
- Verify the image format is supported (JPG, PNG, WEBP)

**"Agent not responding"**
- The first analysis may take 30-60 seconds
- Check your API key has access to Gemini 2.5 Flash
- Try with a smaller image file (<5MB)

**Color recommendations seem off**
- Ensure your photo is well-lit and in focus
- Try uploading from different angles
- Provide additional context in a follow-up message

## 📝 Notes

- **Image Generation**: Uses Google Imagen 3 to generate photorealistic painted miniature renders. Each render takes 30-60 seconds to generate.
- **Paint Prices**: Budget estimates are approximate and may vary by region and retailer
- **Time Estimates**: Actual painting time varies based on individual skill and techniques used
- **Paint Brands**: Recommendations include Citadel, Vallejo, and Army Painter brands
- **API Requirements**: Requires Google AI API key with access to both Gemini 2.5 Flash and Imagen 3

## 🚀 Future Enhancements

Potential improvements for future versions:
- Image-to-image transformation for more accurate painted renders based on the original photo
- Support for batch analysis of multiple miniatures
- Paint inventory tracking
- Progress tracking for painting projects
- Community color scheme sharing
- Video tutorial recommendations
- Download option for generated renders

## 🤝 Contributing

This project is built with Google ADK. To contribute or customize:

1. Fork the repository
2. Modify agent instructions in [agent.py](agent.py)
3. Test with various miniature types
4. Submit improvements

## 📄 License

This project is for educational and personal use. Miniature and paint brand names are property of their respective owners.

## 🙏 Acknowledgments

- Powered by Google Gemini 2.5 Flash
- Built with Google Agent Development Kit (ADK)
- UI created with Streamlit
- Inspired by the miniature painting community

---

**Happy Painting! 🎨**

For questions, issues, or suggestions, please open an issue in the repository.
