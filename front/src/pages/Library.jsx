const handleUpload = async (e) => {
  e.preventDefault();
  if (!file) return;
  
  setUploading(true);
  const formData = new FormData();
  formData.append('file', file);
  
  try {
    const response = await api.post('/api/projects', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    
    setFile(null);
    fetchProjects();
    alert('Файл успешно загружен!');
  } catch (error) {
    console.error('Upload error:', error);
    alert('Ошибка при загрузке файла: ' + (error.response?.data?.detail || error.message));
  } finally {
    setUploading(false);
  }
};