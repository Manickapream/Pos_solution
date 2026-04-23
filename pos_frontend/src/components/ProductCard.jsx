import { useNavigate } from 'react-router-dom'
import { MessageCircle, FileText, IndianRupee } from 'lucide-react'
import './ProductCard.css'

export default function ProductCard({ product }) {
  const navigate = useNavigate()

  const handleEnquiry = () => {
    navigate('/inquiry', { state: { product_name: product.name, price: product.price } })
  }

  return (
    <div className="product-card">
      {/* Price Badge */}
      <div className="product-price-badge">
        <IndianRupee size={13} strokeWidth={2.5} />
        {product.price}
      </div>

      {/* Image */}
      <div className="product-img-wrap">
        {product.image_url ? (
          <img src={product.image_url} alt={product.name} className="product-img" />
        ) : (
          <div className="product-img-placeholder">
            <span>No Image</span>
          </div>
        )}
      </div>

      {/* Info */}
      <div className="product-info">
        <h3 className="product-name">{product.name}</h3>
        {product.description && (
          <p className="product-desc">{product.description}</p>
        )}
      </div>

      {/* Actions */}
      <div className="product-actions">
        <button className="btn btn-primary" onClick={handleEnquiry} id={`enquiry-${product.id}`}>
          <MessageCircle size={15} />
          Enquiry
        </button>
        <button className="btn btn-ghost" id={`doc-${product.id}`}>
          <FileText size={15} />
          Document
        </button>
      </div>
    </div>
  )
}
