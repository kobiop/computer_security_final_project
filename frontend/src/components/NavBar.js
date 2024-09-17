import * as React from 'react';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import Button from '@mui/material/Button';
import { Link } from 'react-router-dom'; // Import Link from react-router-dom

import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const Navbar = () => {
    const pages = [
        { name: 'Add Client', path: '/add-client' },
        { name: 'Clients', path: '/clients' },
        { name: 'Reset password', path: '/login-reset-password' }
    ];
    const navigate = useNavigate();

    // Uncomment and ensure this useEffect is correctly implemented if you need authentication status checking
    // useEffect(() => {
    //     // Function to check authentication status
    //     const checkAuth = async () => {
    //         try {
    //             const response = await axios.get('http://localhost:5000/check-auth', {
    //                 withCredentials: true, // If you are using cookies for authentication
    //             });
    //             setIsLoggedIn(response.data.isLoggedIn); // Assuming your API returns this
    //         } catch (error) {
    //             console.error('Error checking authentication', error);
    //             setIsLoggedIn(false);
    //         }
    //     };

    //     checkAuth();
    // }, []);

    const handleLogout = async () => {
        try {
            const reponse = axios.get('http://localhost:5000/logout', { withCredentials: true });
            navigate("/login");
        } catch (error) {
            console.error('Error logging out', error);
        }
    };

    return (
        <AppBar position="static">
            <Container maxWidth="xl">
                <Toolbar disableGutters>
                    <Typography
                        variant="h6"
                        noWrap
                        component="a"
                        sx={{
                            mr: 2,
                            display: { xs: 'flex' },
                            fontFamily: 'monospace',
                            fontWeight: 700,
                            letterSpacing: '.3rem',
                            color: 'inherit',
                            textDecoration: 'none',
                        }}
                    >
                        CommunicationLTD
                    </Typography>

                    <Box sx={{ flexGrow: 1, display: { xs: 'flex', md: 'flex' } }}>
                        {pages.map((page) => (
                            <Button
                                key={page.name}
                                component={Link}
                                to={page.path} // Use React Router's Link for navigation
                                sx={{ my: 2, color: 'white', display: 'block' }}
                            >
                                {page.name}
                            </Button>
                        ))}
                        <Button
                            onClick={handleLogout}
                            sx={{ my: 2, color: 'white', display: 'block' }}
                        >
                            Logout
                        </Button>
                    </Box>
                </Toolbar>
            </Container>
        </AppBar>
    );
}

export default Navbar;
