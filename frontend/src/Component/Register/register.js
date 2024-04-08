import React, { useState } from 'react';
import './register.css';
import { useNavigate } from 'react-router';

const FormWrapper = ({ children }) => {
  return (
    <div className="form-wrapper">
      {children}
    </div>
  );
};

const Register = () => {
  const initialFormData = {
    user_email: '',
    user_password: '',
    confirmPassword: '',
    user_name: '',
  };

  const [formData, setFormData] = useState(initialFormData);
  const navigate = useNavigate();

  const handleChange = (event) => {
    const { name, value } = event.target;
    setFormData((prevFormData) => ({
      ...prevFormData,
      [name]: value,
    }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    if (formData.user_password !== formData.confirmPassword) {
      alert('Passwords do not match');
      return;
    }

    try {
      const response = await fetch('http://localhost:5000/signup', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (response.ok) {
        alert('Registration successful');
        navigate('/'); // Redirect to login page after successful registration
      } else {
        const data = await response.json();
        alert(data.message || 'Registration failed');
      }
    } catch (error) {
      console.error('Error:', error);
      alert('An error occurred. Please try again later.');
    }
  };

  const renderFormField = (name, type = 'text', label) => {
    return (
      <div className="form-group" key={name}>
        <label htmlFor={name}>{label}</label>
        <input
          type={type}
          id={name}
          name={name}
          value={formData[name]}
          onChange={handleChange}
          placeholder={label}
        />
      </div>
    );
  };

  return (
    <FormWrapper>
      <form id="registrationForm" onSubmit={handleSubmit} className="register">
        {renderFormField('user_email', 'text', 'Email')}
        {renderFormField('user_password', 'password', 'Password')}
        {renderFormField('confirmPassword', 'password', 'Confirm Password')}
        {renderFormField('user_name', 'text', 'Username')}
        <div className="form-group">
          <button type="submit">Submit</button>
        </div>
      </form>
    </FormWrapper>
  );
};

export default Register;
