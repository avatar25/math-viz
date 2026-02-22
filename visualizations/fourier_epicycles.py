import streamlit as st
import streamlit.components.v1 as components
import json
import numpy as np
import cv2
from PIL import Image

def render():
    st.title("Fourier Series (Drawing with Epicycles)")
    st.markdown(r"""
    The **Fourier Transform** is one of the most profound discoveries in mathematics. It states that *any* complex continuous shape or signal can be perfectly decomposed into a series of elegantly spinning circles (sine waves) rotating at different speeds.
    
    In this visualization, we compute the Discrete Fourier Transform (DFT) of a mathematical silhouette. By connecting the centers of these spinning gears (epicycles) mathematically, we can trace beautiful, complex shapes.
    
    Adjust the **Number of Epicycles** below. Notice how a small number gives a crude, fuzzy approximation, while adding higher-frequency harmonics instantly pulls the chaotic line into a razor-sharp, crisp form.
    """, unsafe_allow_html=True)
    
    st.sidebar.header("Fourier Parameters")
    
    shape = st.sidebar.selectbox("Silhouette Shape", ["Heart", "Trefoil Knot", "Infinity (Lemniscate)", "📷 Custom Selfie / Image"])
    
    custom_points_json = "[]"
    num_points_sampled = 300
    
    if shape == "📷 Custom Selfie / Image":
        st.sidebar.markdown("---")
        uploaded_file = st.sidebar.file_uploader("Upload an Image", type=["png", "jpg", "jpeg"])
        # Optional: uncomment to add direct webcam snapshot
        # camera_file = st.sidebar.camera_input("Take a Selfie")
        # if camera_file: uploaded_file = camera_file
        
        if uploaded_file is not None:
            # 1. Image -> OpenCV Array
            image = Image.open(uploaded_file).convert('RGB')
            img_array = np.array(image)
            
            # Image Tuning Parameters
            st.sidebar.markdown("**Image Edge Tuning**")
            canny_low = st.sidebar.slider("Edge Det. Min", min_value=0, max_value=255, value=50, step=5)
            canny_high = st.sidebar.slider("Edge Det. Max", min_value=0, max_value=255, value=150, step=5)
            top_contours_n = st.sidebar.slider("Contours to Combine", min_value=1, max_value=50, value=5, step=1)
            
            # 2. Edge Detection (Canny)
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            edges = cv2.Canny(blurred, canny_low, canny_high)
            
            # 3. Find Contours using RETR_LIST to find internal loops (like car windows)
            contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
            if contours:
                # Sort by length and take the longest N
                contours = sorted(contours, key=len, reverse=True)[:top_contours_n]
                
                # Show a preview of the contour to the user
                st.sidebar.markdown("**Computed Contour Preview:**")
                preview_img = np.zeros_like(img_array)
                cv2.drawContours(preview_img, contours, -1, (0, 255, 255), 2)
                st.sidebar.image(preview_img, use_container_width=True)
                
                # Tie all of the contours together into a single continuous drawing path
                pts_list = []
                for c in contours:
                    pts_list.extend(c.reshape(-1, 2).astype(float))
                pts = np.array(pts_list)
                
                # 4. Interpolate/Downsample to keep the browser fast
                N = 800
                if len(pts) > N:
                    indices = np.linspace(0, len(pts)-1, N, dtype=int)
                    pts = pts[indices]
                elif len(pts) == 0:
                    pts = np.array([[0,0]])
                
                num_points_sampled = len(pts)
                
                # 5. Center and Scale the coordinates to fit the Canvas
                min_x, max_x = np.min(pts[:, 0]), np.max(pts[:, 0])
                min_y, max_y = np.min(pts[:, 1]), np.max(pts[:, 1])
                cx = (min_x + max_x) / 2
                cy = (min_y + max_y) / 2
                pts[:, 0] -= cx
                pts[:, 1] -= cy
                scale = 250.0 / max(max_x - min_x, max_y - min_y, 1)
                pts *= scale
                
                # 6. JSON serialization for JavaScript injection
                json_data = [{"x": float(p[0]), "y": float(p[1])} for p in pts]
                custom_points_json = json.dumps(json_data)
            else:
                st.sidebar.error("Could not trace edges in this image.")
        else:
            st.sidebar.info("Upload an image to compute its Fourier Transform!")
    
    # Send shape as integer to JS
    shape_map = {"Heart": 0, "Trefoil Knot": 1, "Infinity (Lemniscate)": 2, "📷 Custom Selfie / Image": 3}
    shape_id = shape_map[shape]
    
    # The max number of harmonics is bounded by the number of points we sample
    harmonics = st.sidebar.slider("Number of Epicycles (Harmonics)", min_value=1, max_value=num_points_sampled, value=min(150, num_points_sampled), step=1)
    
    speed = st.sidebar.slider("Drawing Speed", min_value=0.1, max_value=5.0, value=1.0, step=0.1)

    p5_html = f"""
    <!DOCTYPE html>
    <html>
      <head>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.9.0/p5.min.js"></script>
        <style>
          body {{
            margin: 0;
            padding: 0;
            overflow: hidden;
            background-color: transparent;
            display: flex;
            justify-content: center;
            align-items: center;
          }}
          canvas {{
            border-radius: 12px;
            box-shadow: 0 10px 40px rgba(0,255,255,0.05);
            width: 800px !important;
            height: 600px !important;
            border: 1px solid rgba(255,255,255,0.1);
          }}
        </style>
      </head>
      <body>
        <script>
          const shapeId = {shape_id};
          let maxHarmonics = {harmonics};
          const speedMulti = {speed};
          
          let time = 0;
          let path = [];
          let fourierTarget = [];

          function dft(x) {{
            let X = [];
            const N = x.length;
            for (let k = 0; k < N; k++) {{
              let re = 0;
              let im = 0;
              for (let n = 0; n < N; n++) {{
                let phi = (TWO_PI * k * n) / N;
                // Complex multiplication: (x_re + i * x_im) * (cos(phi) - i * sin(phi))
                re += x[n].x * cos(phi) + x[n].y * sin(phi);
                im += x[n].y * cos(phi) - x[n].x * sin(phi);
              }}
              re = re / N;
              im = im / N;
              
              let freq = k;
              let amp = sqrt(re * re + im * im);
              let phase = atan2(im, re);
              
              X[k] = {{ re, im, freq, amp, phase }};
            }}
            return X;
          }}

          function setup() {{
            createCanvas(800, 600);
            
            let rawPoints = [];
            
            if (shapeId === 3) {{
              // Parse the injected custom image contour JSON generated by python/OpenCV
              rawPoints = JSON.parse(`{custom_points_json}`);
            }} else {{
              // 1. Sample the mathematical shape
              const N = 300;
              for (let i = 0; i < N; i++) {{
                let t = map(i, 0, N, 0, TWO_PI);
                let bx = 0, by = 0;
                
                if (shapeId === 0) {{
                  // Heart Curve
                  bx = 16 * pow(sin(t), 3);
                  by = -(13 * cos(t) - 5 * cos(2*t) - 2 * cos(3*t) - cos(4*t));
                  bx *= 12; by *= 12; // Scale up
                }} else if (shapeId === 1) {{
                  // Trefoil Knot
                  bx = sin(t) + 2 * sin(2 * t);
                  by = cos(t) - 2 * cos(2 * t);
                  bx *= 60; by *= 60;
                }} else if (shapeId === 2) {{
                  // Lemniscate of Bernoulli (Infinity)
                  let scale = 200;
                  bx = (scale * cos(t)) / (1 + pow(sin(t), 2));
                  by = (scale * sin(t) * cos(t)) / (1 + pow(sin(t), 2));
                }}
                rawPoints.push({{ x: bx, y: by }});
              }}
            }}
            
            // If nothing is loaded, provide a fallback dot
            if (rawPoints.length === 0) {{
                rawPoints.push({{x: 0, y: 0}});
            }}
            
            // 2. Compute the Discrete Fourier Transform
            fourierTarget = dft(rawPoints);
            
            // 3. Sort by amplitude so the largest gears are drawn first
            fourierTarget.sort((a, b) => b.amp - a.amp);
          }}

          function epicycles(x, y, rotation, fourier, maxCircs) {{
            for (let i = 0; i < maxCircs; i++) {{
              if (i >= fourier.length) break;
              
              let prevx = x;
              let prevy = y;
              
              let freq = fourier[i].freq;
              let radius = fourier[i].amp;
              let phase = fourier[i].phase;
              
              x += radius * cos(freq * time + phase + rotation);
              y += radius * sin(freq * time + phase + rotation);
              
              // Draw the subtle spinning gears
              stroke(255, 255, 255, 70);
              noFill();
              strokeWeight(1.5);
              ellipse(prevx, prevy, radius * 2);
              
              // Draw the spoke connecting center to edge
              stroke(150, 255, 255, 180);
              strokeWeight(2.5);
              line(prevx, prevy, x, y);
            }}
            return createVector(x, y);
          }}

          function draw() {{
            background(11, 11, 11);
            
            // Move origin to center
            let vx = epicycles(width / 2, height / 2, 0, fourierTarget, maxHarmonics);
            
            path.unshift(vx);
            
            // Trace the beautiful line
            beginShape();
            noFill();
            
            // Add native glowing shadow effect for HTML canvas
            drawingContext.shadowBlur = 20;
            drawingContext.shadowColor = '#00FFFF';
            
            for (let i = 0; i < path.length; i++) {{
               // Rich, neon cyan glowing stroke
               strokeWeight(4.5);
               // Fade slightly so you can see the head of the drawing clearly against the tail
               stroke(0, 255, 255, map(i, 0, path.length, 255, 60));
               vertex(path[i].x, path[i].y);
            }}
            endShape();
            
            // Turn off shadow for next geometric paints
            drawingContext.shadowBlur = 0;
            
            let dt = TWO_PI / fourierTarget.length;
            time += dt * speedMulti;
            
            // Don't blank out the trail! Just pop the oldest points so it creates a continuous, unbroken, glowing loop
            let maxPoints = Math.floor(TWO_PI / (dt * speedMulti)) + 2;
            if (path.length > maxPoints) {{
              path.pop();
            }}
            
            if (time > TWO_PI) {{
              time = 0;
            }}
          }}
        </script>
      </body>
    </html>
    """
    
    components.html(p5_html, height=650)
