import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Box from '@mui/material/Box';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import Grid from '@mui/material/Grid';
import Container from '@mui/material/Container';
import Button from '@mui/material/Button';
import Navbar from './NavBar';

export default function ClientsPage() {
    const [clients, setClients] = useState([]);

    useEffect(() => {
        fetchClients();
    }, []);

    const fetchClients = async () => {
        try {
            const response = await axios.get('http://localhost:5000/clients');
            setClients(response.data.clients);
        } catch (error) {
            console.error('There was an error fetching the clients!', error);
        }
    };

    const handleDelete = async (clientId) => {
        try {
            await axios.post('http://localhost:5000/delete', { id: clientId }, { withCredentials: true });
            fetchClients();
        } catch (error) {
            console.error('There was an error deleting the client!', error);
        }
    };

    return (
        <>
            <Navbar />

            <Container maxWidth="md">
                <Box sx={{ mt: 4, mb: 4 }}>
                    <Typography
                        variant="h4"
                        component="h1"
                        sx={{
                            fontWeight: 'bold',
                            color: 'text.primary',
                            pb: 1,
                            textAlign: 'left'
                        }}
                    >
                        Clients List
                    </Typography>
                </Box>
                <Grid container spacing={3}>
                    {clients.map(client => (
                        <Grid item xs={12} sm={6} md={4} key={client.id}>
                            <Card sx={{ boxShadow: 3, borderRadius: '12px' }}>
                                <CardContent sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                                    <Typography variant="h6" sx={{ fontWeight: 'bold', mb: 1 }}>
                                        <span dangerouslySetInnerHTML={{ __html: `${client.first_name} ${client.last_name}` }} />
                                    </Typography>
                                    <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
                                        <Typography color="textSecondary" variant="body2">
                                            <strong>Address:</strong>
                                            <span dangerouslySetInnerHTML={{ __html: client.address }} />
                                        </Typography>
                                        <Typography color="textSecondary" variant="body2">
                                            <strong>Email:</strong>
                                            <a href={`mailto:${client.email}`} style={{ color: 'inherit', textDecoration: 'none' }}>
                                                <span dangerouslySetInnerHTML={{ __html: client.email }} />
                                            </a>
                                        </Typography>
                                        <Typography color="textSecondary" variant="body2">
                                            <strong>Phone Number:</strong>
                                            <a href={`tel:${client.phone_number}`} style={{ color: 'inherit', textDecoration: 'none' }}>
                                                <span dangerouslySetInnerHTML={{ __html: client.phone_number }} />
                                            </a>
                                        </Typography>
                                    </Box>

                                    <Button
                                        variant="outlined"  // Changed to 'outlined' for a cleaner look
                                        color="error"
                                        onClick={() => handleDelete(client.id)}
                                        sx={{
                                            mt: 2,
                                            borderRadius: '8px', // Rounded corners
                                            borderColor: 'error.main',
                                            color: 'error.main',
                                            '&:hover': {
                                                borderColor: 'error.dark',
                                                backgroundColor: 'error.light',
                                                color: 'common.white',
                                            },
                                            '&:active': {
                                                borderColor: 'error.main',
                                                backgroundColor: 'error.blue',
                                            }
                                        }}
                                    >
                                        Delete
                                    </Button>
                                </CardContent>
                            </Card>
                        </Grid>
                    ))}
                </Grid>
            </Container>
        </>
    );
}
