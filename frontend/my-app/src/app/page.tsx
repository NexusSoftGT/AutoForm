'use client';

import { useState } from 'react';
import axios from 'axios';

interface FormData {
  policyNo: string;
  certificateNo: string;
  companyId: string;
  firstName: string;
  lastName: string;
  address: string;
  city: string;
}

const Page = () => {
  const [formData, setFormData] = useState<FormData>({
    policyNo: '',
    certificateNo: '',
    companyId: '',
    firstName: '',
    lastName: '',
    address: '',
    city: ''
  });
  const [loading, setLoading] = useState(false);
  const [fullData, setFullData] = useState<string | null>(null);

  // Function to fetch the output from the Flask backend
  const fetchOutput = async () => {
    setLoading(true);
    try {
      // Make the GET request to the Flask backend
      const response = await axios.get('http://127.0.0.1:5000/run-script');
      
      // Assuming response contains the necessary data in JSON format
      const data = response.data.output;
      const parsedData = JSON.parse(data);

      // Split name into first and last name
      const fullName = parsedData["Name"] || '';
      const [firstName = '', lastName = ''] = fullName.split(' ');

      // Set the formData with the extracted data or fallback to empty string
      setFormData({
        policyNo: parsedData["Policy No."] || '',
        certificateNo: parsedData["SL No./Certificate No."] || '',
        companyId: parsedData["Company/TPA ID No."] || '',
        firstName,
        lastName,
        address: parsedData["Address"] || '',
        city: parsedData["City"] || ''
      });

      // Set the full data as a string for display
      setFullData(JSON.stringify(parsedData, null, 2));
    } catch (error) {
      console.error('Error fetching output:', error);
      setFormData({
        policyNo: '',
        certificateNo: '',
        companyId: '',
        firstName: '',
        lastName: '',
        address: '',
        city: ''
      });
      setFullData('An error occurred while fetching the output.');
    } finally {
      setLoading(false);
    }
  };

  // Handle input changes and update the form state
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value
    }));
  };

  return (
    <div className="max-w-lg mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Auto-Populated Form</h1>

      {/* Button to trigger the fetching of output */}
      <button
        onClick={fetchOutput}
        disabled={loading}
        className="w-full bg-blue-500 text-white p-2 rounded-md mt-4"
      >
        {loading ? 'Loading...' : 'Fetch Output from Python'}
      </button>

      {/* Display the full data */}
      {fullData && (
        <div className="mt-6">
          <h2 className="text-lg font-semibold">Full Extracted Data:</h2>
          <pre className="bg-gray-100 p-4 rounded-md">{fullData}</pre>
        </div>
      )}

      {/* Form Fields */}
      <form className="space-y-4 mt-4">
        <div>
          <label htmlFor="policyNo" className="block text-sm font-medium text-gray-700">Policy No.</label>
          <input
            type="text"
            id="policyNo"
            name="policyNo"
            value={formData.policyNo}
            onChange={handleChange}
            className="mt-1 block w-full border border-gray-300 rounded-md p-2"
            placeholder="Policy No."
          />
        </div>

        <div>
          <label htmlFor="certificateNo" className="block text-sm font-medium text-gray-700">SL No./Certificate No.</label>
          <input
            type="text"
            id="certificateNo"
            name="certificateNo"
            value={formData.certificateNo}
            onChange={handleChange}
            className="mt-1 block w-full border border-gray-300 rounded-md p-2"
            placeholder="SL No./Certificate No."
          />
        </div>

        <div>
          <label htmlFor="companyId" className="block text-sm font-medium text-gray-700">Company/TPA ID No.</label>
          <input
            type="text"
            id="companyId"
            name="companyId"
            value={formData.companyId}
            onChange={handleChange}
            className="mt-1 block w-full border border-gray-300 rounded-md p-2"
            placeholder="Company/TPA ID No."
          />
        </div>

        <div>
          <label htmlFor="firstName" className="block text-sm font-medium text-gray-700">First Name</label>
          <input
            type="text"
            id="firstName"
            name="firstName"
            value={formData.firstName}
            onChange={handleChange}
            className="mt-1 block w-full border border-gray-300 rounded-md p-2"
            placeholder="First Name"
          />
        </div>

        <div>
          <label htmlFor="lastName" className="block text-sm font-medium text-gray-700">Last Name</label>
          <input
            type="text"
            id="lastName"
            name="lastName"
            value={formData.lastName}
            onChange={handleChange}
            className="mt-1 block w-full border border-gray-300 rounded-md p-2"
            placeholder="Last Name"
          />
        </div>

        <div>
          <label htmlFor="address" className="block text-sm font-medium text-gray-700">Address</label>
          <input
            type="text"
            id="address"
            name="address"
            value={formData.address}
            onChange={handleChange}
            className="mt-1 block w-full border border-gray-300 rounded-md p-2"
            placeholder="Address"
          />
        </div>

        <div>
          <label htmlFor="city" className="block text-sm font-medium text-gray-700">City</label>
          <input
            type="text"
            id="city"
            name="city"
            value={formData.city}
            onChange={handleChange}
            className="mt-1 block w-full border border-gray-300 rounded-md p-2"
            placeholder="City"
          />
        </div>

        {/* Submit Button */}
        <button
          type="submit"
          className="w-full bg-green-500 text-white p-2 rounded-md mt-4"
        >
          Submit
        </button>
      </form>
    </div>
  );
};

export default Page;
