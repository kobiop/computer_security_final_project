import React, { useState } from 'react';
import axios from 'axios';
import Avatar from '@mui/material/Avatar';
import Button from '@mui/material/Button';
import CssBaseline from '@mui/material/CssBaseline';
import TextField from '@mui/material/TextField';
import Link from '@mui/material/Link';
import Grid from '@mui/material/Grid';
import Box from '@mui/material/Box';
import LockOutlinedIcon from '@mui/icons-material/LockOutlined';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import { useNavigate } from 'react-router-dom';

const defaultTheme = createTheme();

export default function ForgotPassword() {
    const [emailSent, setEmailSent] = useState(false);
    const [email, setEmail] = useState('');
    const [auth_code, setAuthCode] = useState('');
    const [error, setError] = useState(null);
    const navigate = useNavigate();

    const handleEmailSubmit = async (event) => {
        event.preventDefault();
        try {
            const response = await axios.post('http://localhost:5000/forgot-password', { email });
            if (response.status === 200) {
                setEmailSent(true);
                setError(null);
            } else {
                setError('Email not found.');
            }
        } catch (err) {
            if (err.response && err.response.data && err.response.data.message) {
                setError(err.response.data.message);
            } else {
                setError('Failed to reset password. Please try again.');
            }
        }
    };

    const handleAuthCodeSubmit = async (event) => {
        event.preventDefault();
        try {
            const response = await axios.post('http://localhost:5000/verify-auth-code', { email, auth_code });
            if (response.status === 200) {
                navigate('/reset-password', { state: { email } });
            } else {
                setError('Invalid authentication code.');
            }
        } catch (err) {
            setError('Error verifying code.');
        }
    };

    return (
        <ThemeProvider theme={defaultTheme}>
            <Container component="main" maxWidth="xs">
                <CssBaseline />
                <Box
                    sx={{
                        marginTop: 8,
                        display: 'flex',
                        flexDirection: 'column',
                        alignItems: 'center',
                    }}
                >
                    <Avatar sx={{ m: 1, bgcolor: 'secondary.main' }}>
                        <LockOutlinedIcon />
                    </Avatar>
                    <Typography component="h1" variant="h5">
                        Forgot Password
                    </Typography>
                    <Box component="form" onSubmit={emailSent ? handleAuthCodeSubmit : handleEmailSubmit} noValidate sx={{ mt: 1 }}>
                        {!emailSent ? (
                            <TextField
                                margin="normal"
                                required
                                fullWidth
                                id="email"
                                label="Email Address"
                                name="email"
                                autoComplete="email"
                                autoFocus
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                            />
                        ) : (
                            <TextField
                                margin="normal"
                                required
                                fullWidth
                                id="auth_code"
                                label="Authentication Code"
                                name="auth_code"
                                autoComplete="off"
                                autoFocus
                                value={auth_code}
                                onChange={(e) => setAuthCode(e.target.value)}
                            />
                        )}
                        {error && (
                            <Typography color="error" variant="body2">
                                {error}
                            </Typography>
                        )}
                        <Button
                            type="submit"
                            fullWidth
                            variant="contained"
                            sx={{ mt: 3, mb: 2 }}
                        >
                            {emailSent ? 'Verify Code' : 'Send Email'}
                        </Button>
                        <Grid container justifyContent="flex-end">
                            <Grid item>
                                <Link href="/login" variant="body2">
                                    Remembered? Sign In
                                </Link>
                            </Grid>
                        </Grid>
                    </Box>
                </Box>
            </Container>
        </ThemeProvider>
    );
}
