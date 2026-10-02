import { useState } from "react";

import {
  summarizeText
} from "../services/api";

import {
  FileText,
  Sparkles,
  Copy,
  Trash2
} from "lucide-react";


function Summarizer() {

  const [text, setText] =
    useState("");

  const [summary, setSummary] =
    useState("");

  const [loading, setLoading] =
    useState(false);

  const [error, setError] =
    useState("");


  const handleSummarize = async () => {

    if (!text.trim()) {

      setError(
        "Please enter some text."
      );

      return;
    }


    try {

      setLoading(true);

      setError("");

      setSummary("");


      const data =
        await summarizeText(text);


      setSummary(
        data.summary
      );

    }
    catch (err) {

      setError(
        err.message
      );

    }
    finally {

      setLoading(false);

    }

  };


  const handleCopy = async () => {

    if (summary) {

      await navigator.clipboard.writeText(
        summary
      );

    }

  };


  const handleClear = () => {

    setText("");

    setSummary("");

    setError("");

  };


  return (

    <div className="tool-panel">

      <div className="tool-heading">

        <div className="tool-icon">
          <FileText />
        </div>

        <div>

          <h2>
            AI Text Summarizer
          </h2>

          <p>
            Convert long text into a
            clear and concise summary.
          </p>

        </div>

      </div>


      <div className="workspace-grid">

        <div className="workspace-box">

          <div className="box-header">

            <span>
              Input Text
            </span>

            <button
              className="icon-button"
              onClick={handleClear}
            >

              <Trash2 size={18} />

            </button>

          </div>


          <textarea
            value={text}
            onChange={(e) =>
              setText(e.target.value)
            }
            placeholder="
Paste your paragraph,
article or document text here...
            "
          />


          <div className="character-count">

            {text.length} characters

          </div>


          <button
            className="primary-button"
            onClick={handleSummarize}
            disabled={loading}
          >

            <Sparkles size={18} />

            {
              loading
                ? "Generating Summary..."
                : "Summarize"
            }

          </button>


          {
            error &&
            <div className="error-message">

              {error}

            </div>
          }

        </div>


        <div className="workspace-box">

          <div className="box-header">

            <span>
              AI Response
            </span>


            {
              summary &&
              <button
                className="icon-button"
                onClick={handleCopy}
              >

                <Copy size={18} />

              </button>
            }

          </div>


          <div className="ai-output">

            {
              loading
                ? (
                  <div className="loader-container">

                    <div className="loader"></div>

                    <p>
                      Gemini is thinking...
                    </p>

                  </div>
                )

                : summary

                  ? (
                    <p>
                      {summary}
                    </p>
                  )

                  : (
                    <div className="empty-state">

                      <Sparkles size={40} />

                      <p>
                        Your AI generated
                        summary will appear here.
                      </p>

                    </div>
                  )
            }

          </div>

        </div>

      </div>

    </div>

  );

}

export default Summarizer;