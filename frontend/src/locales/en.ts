export default {
  app: {
    title: 'Anything Summary',
    subtitle: 'One-stop intelligent content summary tool, supporting multi-modal mixed input',
    guide: 'Guide',
    contact: 'Contact Us'
  },
  features: {
    text: 'Text',
    webpage: 'Web',
    document: 'Doc',
    audio: 'Audio',
    video: 'Video',
    archive: 'Archive'
  },
  input: {
    url: {
      placeholder: 'Enter webpage URL',
      add: 'Add URL',
      invalid: 'Please enter a valid URL, e.g., https://www.example.com'
    },
    text: {
      placeholder: 'Enter or paste text content',
      add: 'Add Text'
    },
    delete: 'Delete',
    file: {
      title: 'Drop files here or click to browse',
      maxSize: 'Maximum file size: 100MB',
      allowedTypes: 'Supported formats',
      button: 'Select Files'
    }
  },
  actions: {
    submit: 'Summarize',
    copy: 'Copy',
    download: 'Download',
    regenerate: 'Regenerate'
  },
  status: {
    processing: 'Generating summary...',
    empty: 'Enter content on the left and click "Summarize" to generate summary'
  },
  contact: {
    title: 'Contact Us',
    email: 'Email: support@anythingsummary.com',
    github: 'GitHub: anything-summary',
    wechat: 'WeChat Official Account: AnythingSummary',
    feedback: 'Welcome to provide feedback or suggestions to help us do better!',
    close: 'Close'
  },
  guide: {
    title: 'How to Use',
    sections: {
      input: {
        title: 'Input Methods',
        text: 'Enter or paste text directly',
        url: 'Input webpage URLs for automatic content extraction',
        file: 'Upload files (supports multiple formats)'
      },
      formats: {
        title: 'Supported Formats',
        docs: 'Documents: PDF, Word, TXT',
        images: 'Images: JPG, PNG, GIF (with OCR)',
        audio: 'Audio: MP3, WAV (with speech recognition)',
        video: 'Video: MP4, AVI (extracts audio for transcription)',
        archive: 'Archives: ZIP, RAR, 7Z (auto-extracts content)'
      },
      process: {
        title: 'Generate Summary',
        step1: 'Ensure at least one type of content is provided (text, URL, or file)',
        step2: 'Click the "Summarize" button',
        step3: 'Wait for processing (time depends on content length and type)'
      },
      results: {
        title: 'Handle Results',
        description: 'After getting the summary, you can:',
        copy: 'Copy: One-click copy to clipboard',
        download: 'Download: Save as TXT file',
        regenerate: 'Regenerate: Create a new summary if needed'
      },
      tips: {
        title: 'Usage Tips',
        quality: 'Clearer input content leads to better summary quality',
        length: 'For long texts, consider splitting into paragraphs for better results',
        files: 'Ensure good file quality (clear images, clean audio, etc.)'
      }
    }
  },
  messages: {
    copySuccess: 'Copied successfully!',
    copyFailed: 'Copy failed, please copy manually',
    uploadError: 'File upload failed',
    processingError: 'Processing failed, please try again',
    timeout: 'Request timed out, please try again'
  },
  uppy: {
    dropPaste: 'Drop files here or %{browse}',
    browse: 'browse',
    uploadComplete: 'Upload complete',
    uploadFailed: 'Upload failed',
    dataUploadXFiles: 'Uploading %{smart_count} file||Uploading %{smart_count} files',
    xFilesSelected: {
      0: '%{smart_count} file selected',
      1: '%{smart_count} files selected'
    },
    dropHint: 'Drop your files here',
    fileSource: 'Source: %{name}',
    myDevice: 'My Device',
    chooseFiles: 'Choose files',
    orDragDrop: 'or drag and drop',
    filesUploadedOfTotal: {
      0: '%{complete} of %{smart_count} file uploaded',
      1: '%{complete} of %{smart_count} files uploaded'
    },
    maxFileSize: 'Maximum file size: %{size}',
    removeFile: 'Remove file'
  }
} 