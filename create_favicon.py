#!/usr/bin/env python3
"""
Favicon Generator for Autonomous Task Bot
Created by Syed Fahim
"""

import os
from pathlib import Path

def create_svg_favicon():
    """Create SVG favicon"""
    svg_content = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="32" height="32">
  <!-- Background circle -->
  <circle cx="16" cy="16" r="15" fill="#2563eb" stroke="#1d4ed8" stroke-width="2"/>
  
  <!-- Robot head -->
  <rect x="8" y="6" width="16" height="20" rx="3" fill="#f8fafc" stroke="#1e293b" stroke-width="1"/>
  
  <!-- Eyes -->
  <circle cx="11" cy="12" r="2" fill="#1e293b"/>
  <circle cx="21" cy="12" r="2" fill="#1e293b"/>
  
  <!-- Eye highlights -->
  <circle cx="10.5" cy="11.5" r="0.5" fill="#ffffff"/>
  <circle cx="20.5" cy="11.5" r="0.5" fill="#ffffff"/>
  
  <!-- Mouth -->
  <rect x="12" y="18" width="8" height="2" rx="1" fill="#1e293b"/>
  
  <!-- Antenna -->
  <line x1="16" y1="6" x2="16" y2="2" stroke="#1e293b" stroke-width="2"/>
  <circle cx="16" cy="2" r="1" fill="#ef4444"/>
  
  <!-- Circuit pattern -->
  <path d="M4 8 L8 8 M4 12 L8 12 M4 16 L8 16" stroke="#64748b" stroke-width="1" opacity="0.6"/>
  <path d="M24 8 L28 8 M24 12 L28 12 M24 16 L28 16" stroke="#64748b" stroke-width="1" opacity="0.6"/>
  
  <!-- AI brain pattern -->
  <path d="M14 22 L18 22 M14 24 L18 24 M14 26 L18 26" stroke="#3b82f6" stroke-width="1" opacity="0.8"/>
</svg>'''
    
    static_dir = Path("static")
    static_dir.mkdir(exist_ok=True)
    
    favicon_path = static_dir / "favicon.svg"
    with open(favicon_path, "w") as f:
        f.write(svg_content)
    
    print(f"✅ Created: {favicon_path}")
    return favicon_path

def create_placeholder_ico():
    """Create a placeholder ICO file (since we can't generate binary ICO directly)"""
    ico_content = """# This is a placeholder for favicon.ico
# In a real implementation, you would use a library like Pillow to create a proper ICO file
# For now, the SVG favicon will be used by modern browsers
"""
    
    static_dir = Path("static")
    static_dir.mkdir(exist_ok=True)
    
    ico_path = static_dir / "favicon.ico"
    with open(ico_path, "w") as f:
        f.write(ico_content)
    
    print(f"⚠️  Created placeholder: {ico_path}")
    print("   Note: For a proper ICO file, use an online converter or image editing software")
    return ico_path

def update_html_template():
    """Update the HTML template to include favicon links"""
    template_path = Path("templates/dashboard.html")
    
    if not template_path.exists():
        print("❌ HTML template not found")
        return
    
    # Read the template
    with open(template_path, "r") as f:
        content = f.read()
    
    # Check if favicon links already exist
    if 'rel="icon"' in content:
        print("✅ Favicon links already present in HTML template")
        return
    
    # Add favicon links after the title tag
    favicon_links = '''
    <!-- Favicon -->
    <link rel="icon" type="image/svg+xml" href="/static/favicon.svg">
    <link rel="icon" type="image/x-icon" href="/static/favicon.ico">
    <link rel="apple-touch-icon" href="/static/favicon.svg">
    '''
    
    # Insert favicon links after title
    title_end = content.find('</title>')
    if title_end != -1:
        new_content = content[:title_end + 8] + favicon_links + content[title_end + 8:]
        
        with open(template_path, "w") as f:
            f.write(new_content)
        
        print("✅ Updated HTML template with favicon links")
    else:
        print("❌ Could not find title tag in HTML template")

def main():
    """Main function to create favicon files"""
    print("🤖 Creating favicon for Autonomous Task Bot")
    print("=" * 50)
    
    # Create SVG favicon
    svg_path = create_svg_favicon()
    
    # Create placeholder ICO
    ico_path = create_placeholder_ico()
    
    # Update HTML template
    update_html_template()
    
    print("\n" + "=" * 50)
    print("🎉 Favicon creation completed!")
    print("\n📋 Files created:")
    print(f"   ✅ {svg_path}")
    print(f"   ⚠️  {ico_path} (placeholder)")
    print("   ✅ HTML template updated")
    
    print("\n📝 Next steps:")
    print("   1. For a proper ICO file, convert the SVG using an online tool")
    print("   2. Replace the placeholder favicon.ico with the converted file")
    print("   3. Deploy the updated files to your server")
    print("   4. Clear browser cache to see the new favicon")
    
    print("\n🌐 Online favicon converters:")
    print("   • https://convertio.co/svg-ico/")
    print("   • https://favicon.io/favicon-converter/")
    print("   • https://www.favicon-generator.org/")

if __name__ == "__main__":
    main() 