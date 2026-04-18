import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { Save, ArrowLeft, Upload } from 'lucide-react'
import toast from 'react-hot-toast'
import Sidebar from '../components/Sidebar'
import api from '../api/axios'
import './ProductForm.css'

export default function AddProduct() {
  const [form, setForm] = useState({ name: '', price: '', description: '', status: 'Active' })
  const [image, setImage] = useState(null)
  const [preview, setPreview] = useState(null)
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()
  const role = sessionStorage.getItem('user_role') || 'User'

  useEffect(() => {
    if (role !== 'Admin') {
      toast.error('Access denied. Admin role required.')
      navigate('/admin/dashboard')
    }
  }, [role, navigate])

  const handleChange = e => setForm({ ...form, [e.target.name]: e.target.value })

  const handleImage = e => {
    const file = e.target.files[0]
    if (!file) return
    if (file.size > 2 * 1024 * 1024) { toast.error('Image must be under 2MB'); return }
    const allowed = ['image/jpeg', 'image/png', 'image/webp']
    if (!allowed.includes(file.type)) { toast.error('Only JPG, PNG, WEBP allowed'); return }
    setImage(file)
    setPreview(URL.createObjectURL(file))
  }

  const handleSubmit = async e => {
    e.preventDefault()
    if (!form.name || !form.price) { toast.error('Name and price are required'); return }
    setLoading(true)
    try {
      const fd = new FormData()
      Object.entries(form).forEach(([k, v]) => fd.append(k, v))
      if (image) fd.append('image', image)
      await api.post('products/', fd, { headers: { 'Content-Type': 'multipart/form-data' } })
      toast.success('Product added successfully!')
      navigate('/admin/products')
    } catch {
      toast.error('Failed to add product')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="admin-layout">
      <Sidebar />
      <main className="admin-main">
        <div className="page-header">
          <div>
            <h1>Add Product</h1>
            <p className="page-sub">Fill in the product details below</p>
          </div>
          <button className="btn btn-ghost" onClick={() => navigate('/admin/products')} id="backBtn">
            <ArrowLeft size={16} /> Back
          </button>
        </div>

        <div className="form-card">
          <form onSubmit={handleSubmit} className="product-form">
            <div className="form-row">
              {/* Left column */}
              <div className="form-col">
                <div className="form-group">
                  <label htmlFor="name">Product Name *</label>
                  <input id="name" name="name" type="text" className="form-control"
                    placeholder="e.g. Fanuc 31i Controller"
                    value={form.name} onChange={handleChange} required />
                </div>
                <div className="form-group">
                  <label htmlFor="price">Price *</label>
                  <input id="price" name="price" type="text" className="form-control"
                    placeholder="e.g. 3Lac or 18000"
                    value={form.price} onChange={handleChange} required />
                </div>
                <div className="form-group">
                  <label htmlFor="description">Description</label>
                  <textarea id="description" name="description" className="form-control"
                    rows="4" placeholder="Describe the product..."
                    value={form.description} onChange={handleChange} />
                </div>
                <div className="form-group">
                  <label htmlFor="status">Status</label>
                  <select id="status" name="status" className="form-control"
                    value={form.status} onChange={handleChange}>
                    <option value="Active">Active</option>
                    <option value="Inactive">Inactive</option>
                  </select>
                </div>
              </div>

              {/* Right column – image */}
              <div className="form-col">
                <div className="form-group">
                  <label>Product Image</label>
                  <label className="img-upload-zone" htmlFor="imageInput">
                    {preview ? (
                      <img src={preview} alt="Preview" className="img-preview" />
                    ) : (
                      <div className="upload-placeholder">
                        <Upload size={32} />
                        <span>Click to upload image</span>
                        <small>JPG, PNG, WEBP · Max 2MB</small>
                      </div>
                    )}
                  </label>
                  <input id="imageInput" type="file" accept="image/*"
                    onChange={handleImage} hidden />
                </div>
              </div>
            </div>

            <div className="form-actions">
              <button type="submit" className="btn btn-primary" disabled={loading} id="saveBtn">
                {loading ? <><div className="spinner-sm" /> Saving...</> : <><Save size={16} /> Save Product</>}
              </button>
              <button type="button" className="btn btn-ghost" onClick={() => navigate('/admin/products')}>
                Cancel
              </button>
            </div>
          </form>
        </div>
      </main>
    </div>
  )
}
