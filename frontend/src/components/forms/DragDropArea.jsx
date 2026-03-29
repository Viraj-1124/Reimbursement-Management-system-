import { UploadCloud } from 'lucide-react';
import { useState } from 'react';

export default function DragDropArea({ onFileSelect }) {
  const [isDragging, setIsDragging] = useState(false);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setIsDragging(true);
    } else if (e.type === 'dragleave') {
      setIsDragging(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      onFileSelect(e.dataTransfer.files[0]);
    }
  };

  const handleChange = (e) => {
    e.preventDefault();
    if (e.target.files && e.target.files.length > 0) {
      onFileSelect(e.target.files[0]);
    }
  };

  return (
    <div
      onDragEnter={handleDrag}
      onDragLeave={handleDrag}
      onDragOver={handleDrag}
      onDrop={handleDrop}
      style={{
        border: `2px dashed ${isDragging ? 'var(--color-accent)' : 'var(--color-border)'}`,
        background: isDragging ? '#e8f4f3' : 'transparent',
        padding: '3rem 2rem',
        borderRadius: 'var(--radius-lg)',
        textAlign: 'center',
        cursor: 'pointer',
        transition: 'all 0.2s ease',
      }}
      onClick={() => document.getElementById('file-upload').click()}
    >
      <input 
        id="file-upload" 
        type="file" 
        accept="image/*,.pdf"
        style={{ display: 'none' }} 
        onChange={handleChange} 
      />
      <UploadCloud size={48} color={isDragging ? 'var(--color-accent)' : 'var(--color-text-muted)'} style={{ margin: '0 auto 1rem auto' }} />
      <h3 style={{ margin: '0 0 0.5rem 0', color: isDragging ? 'var(--color-accent)' : 'inherit' }}>
        {isDragging ? 'Drop receipt here' : 'Drop receipt to run AI Extraction'}
      </h3>
      <p className="text-muted" style={{ margin: 0, fontSize: '0.9rem' }}>Supports JPG, PNG, PDF</p>
    </div>
  );
}
