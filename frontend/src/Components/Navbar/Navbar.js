import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';

import Grid2 from '@mui/material/Unstable_Grid2';
import {Link, NavLink } from "react-router-dom";
import MenuItem from '@mui/material/MenuItem'
import Menu from '@mui/material/Menu';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';


const NavBar = () => {
    return (
        <AppBar position="static">
            <Toolbar>
            <Grid2 container spacing={2}>
                <Grid2 size={4}>
                    <Button color="inherit">
                        <Typography sx={{ color: "#000000"}} variant="h5" component="div">
                            Device Viewer
                        </Typography>
                    </Button>
                </Grid2>
                <Grid2 size={2}>
                    <Link to="/">
                        <Button color='inherit'>
                            <Typography variant="h6" sx={{ color: "#FFFFFF"}} component="div">Devices </Typography>
                        </Button>
                    </Link>   
                </Grid2>
                <Grid2 size={2}>
                    <Link to="/dashboard">
                        <Button color="inherit">
                                <Typography variant="h6" sx={{ color: "#FFFFFF"}} component="div">Dashboard</Typography>
                        </Button>
                    </Link>
                </Grid2>

            </Grid2>
            </Toolbar>
        </AppBar>
    )
}

export default NavBar;