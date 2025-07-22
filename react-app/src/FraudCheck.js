import React, { useState } from 'react';
import axios from 'axios';

function FraudCheck() {
  const [form, setForm] = useState({
    zip: '',
    merchant_city: '',
    merchant_state: '',
    mcc: '',
    use_chip_Online_Transaction: false,
    amount: '',
    use_chip_Swipe_Transaction: false,
    use_chip_Chip_Transaction: false
  });
  const [result, setResult] = useState('');

  const handleChange = e => {
    const { name, value, type, checked } = e.target;
    setForm(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleSubmit = async e => {
    e.preventDefault();
    try {
      const token = localStorage.getItem('token');
      const res = await axios.post('http://localhost:8000/predict', {
        ...form,
        zip: parseFloat(form.zip),
        mcc: parseInt(form.mcc),
        amount: parseFloat(form.amount)
      }, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setResult(`Fraud Prediction: ${res.data.fraud_prediction}`);
    } catch (err) {
      setResult(err.response?.data?.detail || 'Prediction failed');
    }
  };

  return (
    <div>
      <h2>Transaction Fraud Check</h2>
      <form onSubmit={handleSubmit}>
        <input name="zip" type="text" placeholder="Zip" value={form.zip} onChange={handleChange} required />
        <input name="merchant_city" type="text" placeholder="Merchant City" value={form.merchant_city} onChange={handleChange} required />
        <input name="merchant_state" type="text" placeholder="Merchant State" value={form.merchant_state} onChange={handleChange} required />
        <input name="mcc" type="text" placeholder="MCC" value={form.mcc} onChange={handleChange} required />
        <input name="amount" type="text" placeholder="Amount" value={form.amount} onChange={handleChange} required />
        <label>
          Online Transaction
          <input name="use_chip_Online_Transaction" type="checkbox" checked={form.use_chip_Online_Transaction} onChange={handleChange} />
        </label>
        <label>
          Swipe Transaction
          <input name="use_chip_Swipe_Transaction" type="checkbox" checked={form.use_chip_Swipe_Transaction} onChange={handleChange} />
        </label>
        <label>
          Chip Transaction
          <input name="use_chip_Chip_Transaction" type="checkbox" checked={form.use_chip_Chip_Transaction} onChange={handleChange} />
        </label>
        <button type="submit">Check Fraud</button>
      </form>
      <p>{result}</p>
      <button onClick={() => { localStorage.removeItem('token'); window.location.href = '/login'; }}>Logout</button>
    </div>
  );
}

export default FraudCheck;
