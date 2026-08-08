import { useRef, useState } from "react";
import { Upload, FileText, X, CheckCircle } from "lucide-react";

function UploadDocument() {

  const fileInputRef = useRef(null);

  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState("");

  const selectFile = (event) => {

    const selectedFile = event.target.files[0];

    if (!selectedFile) {
      return;
    }

    setFile(selectedFile);
    setMessage("");
  };


  const removeFile = () => {

    setFile(null);

    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }

    setMessage("");
  };


  const uploadFile = async () => {

    if (!file) {
      setMessage("Please select a document first.");
      return;
    }

    setUploading(true);
    setMessage("");

    try {

      const formData = new FormData();

      formData.append("file", file);


      const response = await fetch(
        "http://localhost:8000/upload",
        {
          method: "POST",
          body: formData
        }
      );


      if (!response.ok) {
        throw new Error("Upload failed");
      }


      const data = await response.json();

      console.log(data);

      setMessage("Document uploaded successfully.");

      setFile(null);

      if (fileInputRef.current) {
        fileInputRef.current.value = "";
      }

    } catch (error) {

      console.error(error);

      setMessage(
        "Could not upload document. Please check the backend."
      );

    } finally {

      setUploading(false);

    }
  };


  return (

    <div className="upload-card">

      <div className="upload-header">

        <div>

          <h2>Upload Document</h2>

          <p>
            Add documents to your enterprise knowledge base.
          </p>

        </div>

        <Upload size={22} />

      </div>


      <div
        className="upload-area"
        onClick={() => fileInputRef.current.click()}
      >

        <Upload size={35} />

        <h3>
          Drop your document here
        </h3>

        <p>
          or click to browse files
        </p>

        <span>
          PDF, DOCX or TXT
        </span>

        <input
          ref={fileInputRef}
          type="file"
          accept=".pdf,.docx,.txt"
          onChange={selectFile}
          hidden
        />

      </div>


      {file && (

        <div className="selected-file">

          <div className="file-info">

            <FileText size={20} />

            <div>

              <strong>
                {file.name}
              </strong>

              <span>
                {(file.size / 1024 / 1024).toFixed(2)} MB
              </span>

            </div>

          </div>


          <button
            className="remove-file"
            onClick={removeFile}
          >
            <X size={17} />
          </button>

        </div>

      )}


      <button
        className="upload-submit"
        onClick={uploadFile}
        disabled={uploading}
      >

        {uploading ? (
          "Uploading..."
        ) : (
          <>
            <Upload size={17} />
            Upload Document
          </>
        )}

      </button>


      {message && (

        <div className="upload-message">

          {message.includes("successfully") && (
            <CheckCircle size={17} />
          )}

          <span>
            {message}
          </span>

        </div>

      )}

    </div>

  );
}

export default UploadDocument;