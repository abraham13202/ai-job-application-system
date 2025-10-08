#!/bin/bash

# AI Job Application System - Setup Script
# This script sets up the environment and dependencies

echo "=========================================="
echo "🚀 AI Job Application System Setup"
echo "=========================================="
echo ""

# Check Python version
echo "📋 Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Error: Python 3.8 or higher is required"
    echo "   Current version: $python_version"
    exit 1
fi

echo "✅ Python $python_version detected"
echo ""

# Create virtual environment
echo "📦 Creating virtual environment..."
if [ -d "venv" ]; then
    echo "⚠️  Virtual environment already exists. Skipping..."
else
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi
echo ""

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate
echo "✅ Virtual environment activated"
echo ""

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt
echo "✅ Dependencies installed"
echo ""

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p applications_batch applications_comprehensive templates chrome_extension
touch applications_batch/.gitkeep applications_comprehensive/.gitkeep
echo "✅ Directories created"
echo ""

# Create config file from template
if [ ! -f "config.yaml" ]; then
    echo "⚙️  Creating config file..."
    if [ -f "config.template.yaml" ]; then
        cp config.template.yaml config.yaml
        echo "✅ config.yaml created from template"
        echo "   Please edit config.yaml with your information"
    else
        echo "⚠️  config.template.yaml not found, skipping..."
    fi
else
    echo "⚠️  config.yaml already exists, skipping..."
fi
echo ""

# Create resume data template if it doesn't exist
if [ ! -f "resume_data.json" ]; then
    echo "📝 Creating resume data template..."
    cat > resume_data.json << 'EOF'
{
  "name": "Your Name",
  "email": "your.email@example.com",
  "phone": "+1234567890",
  "location": "City, Country",
  "linkedin": "https://linkedin.com/in/yourprofile",
  "github": "https://github.com/yourusername",

  "summary": "Brief professional summary about yourself",

  "education": [
    {
      "degree": "Bachelor of Science in Computer Science",
      "institution": "Your University",
      "location": "City, Country",
      "graduation_date": "2024",
      "gpa": "3.8/4.0"
    }
  ],

  "skills": [
    "Python",
    "Java",
    "Machine Learning",
    "Data Analysis",
    "SQL",
    "TensorFlow",
    "PyTorch",
    "Git"
  ],

  "experience": [
    {
      "title": "Software Engineering Intern",
      "company": "Company Name",
      "location": "City, Country",
      "start_date": "Jun 2023",
      "end_date": "Aug 2023",
      "responsibilities": [
        "Developed features using Python and React",
        "Collaborated with team of 5 engineers",
        "Improved performance by 20%"
      ]
    }
  ],

  "projects": [
    {
      "name": "Project Name",
      "description": "Brief description of the project",
      "technologies": ["Python", "TensorFlow", "Flask"],
      "link": "https://github.com/yourusername/project"
    }
  ],

  "certifications": [
    {
      "name": "AWS Certified Developer",
      "issuer": "Amazon Web Services",
      "date": "2024"
    }
  ]
}
EOF
    echo "✅ resume_data.json template created"
    echo "   Please edit resume_data.json with your information"
else
    echo "⚠️  resume_data.json already exists, skipping..."
fi
echo ""

echo "=========================================="
echo "✅ Setup Complete!"
echo "=========================================="
echo ""
echo "📝 Next Steps:"
echo ""
echo "1. Edit resume_data.json with your information"
echo "2. (Optional) Edit config.yaml to customize search settings"
echo "3. Start the web dashboard:"
echo "   source venv/bin/activate"
echo "   python web_app.py"
echo ""
echo "4. Or run a job search:"
echo "   python comprehensive_search.py"
echo ""
echo "📚 Documentation: See README.md for detailed usage"
echo ""
echo "🎉 Happy job hunting!"
echo "=========================================="
