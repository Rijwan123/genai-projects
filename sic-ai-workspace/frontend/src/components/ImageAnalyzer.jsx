import { useEffect, useState } from "react";

import { explainImage } from "../services/api";

import {
  Image,
  Upload,
  Sparkles,
  X
} from "lucide-react";


function ImageAnalyzer() {

  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState("");
  const [explanation, setExplanation] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");


  // Clean up image preview URL
  useEffect(() => {

    return () => {

      if (preview) {
        URL.revokeObjectURL(preview);
      }

    };

  }, [preview]);


  const handleFile = (event) => {

    const selectedFile = event.target.files?.[0];

    if (!selectedFile) {
      return;
    }


    if (!selectedFile.type.startsWith("image/")) {

      setError("Please select a valid image file.");

      return;
    }


    // Remove previous preview
    if (preview) {
      URL.revokeObjectURL(preview);
    }


    const previewUrl =
      URL.createObjectURL(selectedFile);


    setFile(selectedFile);
    setPreview(previewUrl);

    setExplanation("");
    setError("");

  };


  const handleRemove = () => {

    if (preview) {
      URL.revokeObjectURL(preview);
    }

    setFile(null);
    setPreview("");
    setExplanation("");
    setError("");

  };


  const handleAnalyze = async () => {

    if (!file) {

      setError(
        "Please upload an image first."
      );

      return;

    }


    try {

      setLoading(true);

      setError("");

      setExplanation("");


      const data =
        await explainImage(file);


      setExplanation(
        data.explanation
      );

    }
    catch (err) {

      setError(
        err.message ||
        "Unable to analyze image."
      );

    }
    finally {

      setLoading(false);

    }

  };


  return (

    <div className="tool-panel">

      {/* HEADER */}

      <div className="tool-heading">

        <div className="tool-icon">
          <Image size={24} />
        </div>

        <div>

          <h2>
            Image Intelligence
          </h2>

          <p>
            Upload an image and let Gemini
            understand its contents.
          </p>

        </div>

      </div>


      <div className="workspace-grid">


        {/* LEFT SIDE */}

        <div className="workspace-box">


          {!preview ? (

            /*
              Putting the input INSIDE the label means
              the entire upload area is clickable.
            */

            <label className="upload-area">

              <Upload
                size={52}
                className="upload-icon"
              />

              <h3>
                Upload an image
              </h3>

              <p>
                JPG, JPEG, PNG or WEBP
              </p>

              <span className="upload-button">
                Select Image
              </span>


              <input
                type="file"
                accept="image/png,image/jpeg,image/webp"
                onChange={handleFile}
                className="file-input"
              />

            </label>

          ) : (

            <div className="image-preview-container">

              <button
                className="remove-image-button"
                onClick={handleRemove}
                title="Remove image"
              >
                <X size={18} />
              </button>


              <img
                src={preview}
                alt="Selected preview"
                className="image-preview"
              />


              <div className="image-information">

                <strong>
                  {file?.name}
                </strong>

                <span>
                  {file
                    ? `${(
                        file.size /
                        1024 /
                        1024
                      ).toFixed(2)} MB`
                    : ""}
                </span>

              </div>

            </div>

          )}


          <button
            className="primary-button"
            onClick={handleAnalyze}
            disabled={loading || !file}
          >

            <Sparkles size={18} />

            {loading
              ? "Analyzing Image..."
              : "Analyze Image"}

          </button>


          {error && (

            <div className="error-message">
              {error}
            </div>

          )}

        </div>


        {/* RIGHT SIDE */}

        <div className="workspace-box">

          <div className="box-header">
            <span>AI Analysis</span>
          </div>


          <div className="ai-output">

            {loading ? (

              <div className="loader-container">

                <div className="loader"></div>

                <p>
                  Gemini is analyzing your image...
                </p>

              </div>

            ) : explanation ? (

              <p>
                {explanation}
              </p>

            ) : (

              <div className="empty-state">

                <Image size={45} />

                <p>
                  Image analysis will appear here.
                </p>

              </div>

            )}

          </div>

        </div>


      </div>

    </div>

  );

}


export default ImageAnalyzer;