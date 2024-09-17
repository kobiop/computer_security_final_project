import React, { useState } from 'react';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import Grid from '@mui/material/Grid';
import Typography from '@mui/material/Typography';
import axios from 'axios';
import Navbar from './NavBar'; // Adjust the path according to your project structure
import DOMPurify from 'dompurify';
import { useNavigate } from 'react-router-dom';

export default function AddClientForm() {

    const [error, setError] = useState(null);
    // State to handle form inputs
    const navigate = useNavigate();
    const [clientData, setClientData] = useState({
        firstName: '',
        lastName: '',
        email: '',
        phoneNumber: '',
        address: ''
    });

    // Handle form input change
    const handleInputChange = (event) => {
        const { name, value } = event.target;
        setClientData({ ...clientData, [name]: value });
    };

    // Handle form submission
    const handleSubmit = async (event) => {
        event.preventDefault();
        try {
            const response = await axios.post('http://localhost:5000/add-client', {
                clientData: clientData
            });

            if (response.status === 200) {
                console.log('Client added successfully');
                setClientData({
                    firstName: '',
                    lastName: '',
                    email: '',
                    phoneNumber: '',
                    address: ''
                });
                setError(null);
                navigate("/clients")

            } else {
                console.error('Failed to add client');
            }
        } catch (err) {
            if (err.response && err.response.data && err.response.data.message) {
                setError(err.response.data.message);
            } else {
                setError('Failed to add client. Please try again.');
            }
        }
    };

    return (
        <>
            <Navbar />
            <Box
                component="form"
                onSubmit={handleSubmit}
                sx={{
                    maxWidth: 500,
                    mx: 'auto',
                    mt: 4,
                    p: 2,
                    backgroundColor: 'background.paper',
                    borderRadius: 2,
                    boxShadow: 1,
                }}
            >
                <Typography variant="h5" component="h2" gutterBottom>
                    Add New Client
                </Typography>
                <Grid container spacing={2}>
                    <Grid item xs={12} sm={6}>
                        <TextField
                            required
                            fullWidth
                            label="First Name"
                            name="firstName"
                            value={clientData.firstName}
                            onChange={handleInputChange}
                        />
                    </Grid>
                    <Grid item xs={12} sm={6}>
                        <TextField
                            required
                            fullWidth
                            label="Last Name"
                            name="lastName"
                            value={clientData.lastName}
                            onChange={handleInputChange}
                        />
                    </Grid>
                    <Grid item xs={12}>
                        <TextField
                            required
                            fullWidth
                            label="Email"
                            name="email"
                            value={clientData.email}
                            onChange={handleInputChange}
                            type="email"
                        />
                    </Grid>
                    <Grid item xs={12}>
                        <TextField
                            required
                            fullWidth
                            label="Phone Number"
                            name="phoneNumber"
                            value={clientData.phoneNumber}
                            onChange={handleInputChange}
                            type="tel"
                        />
                    </Grid>
                    <Grid item xs={12}>
                        <TextField
                            required
                            fullWidth
                            label="Address"
                            name="address"
                            value={clientData.address}
                            onChange={handleInputChange}
                        />
                    </Grid>
                </Grid>
                <Box sx={{ mt: 3 }}>
                    <Button
                        type="submit"
                        variant="contained"
                        color="primary"
                        fullWidth
                    >
                        Add Client
                    </Button>
                </Box>
                {error && (
                    <Typography color="error" sx={{ mt: 2 }}>
                        {error}
                    </Typography>
                )}
            </Box>
        </>
    );
}
