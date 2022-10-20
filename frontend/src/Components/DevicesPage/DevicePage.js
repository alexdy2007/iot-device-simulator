import { useState, useEffect, useContext } from 'react';
import DeviceCard from '../DeviceCard/DeviceCard'
import { getDevicesMetaData, deleteAllDevices } from '../../Api/devives'
import {SnackbarContext} from "../../Contexts/SnackBarAlertContext"
import CreateDevice from '../CreateDevice/CreateDevice'

import Grid from '@mui/material/Unstable_Grid2';
import Paper from '@mui/material/Paper';

import Accordion from '@mui/material/Accordion';
import AccordionDetails from '@mui/material/AccordionDetails';
import AccordionSummary from '@mui/material/AccordionSummary';
import Typography from '@mui/material/Typography';

import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import AddCircleIcon from '@mui/icons-material/AddCircle';
import IconButton from '@mui/material/IconButton'
import DeleteIcon from "@mui/icons-material/Delete";
import SaveIcon from '@mui/icons-material/Save';


const DevicePage = () => {

    const [deviceMetaData, setDeviceMetaData] = useState([]);
    const [createDevice, setCreateDevice] = useState(false);
    const {snackbar, setSnackbar} = useContext(SnackbarContext);

    const createDeviceChange = () => {
        setCreateDevice(!createDevice);
    };

    const getDeviceMetaDataCallback = () =>{
        getDevicesMetaData()
        .then((deviceData) => {
            setDeviceMetaData(deviceData)
        })
    }

    const deleteAllDevicesCall = () => {
        deleteAllDevices()
        .then(() => {
            setDeviceMetaData([])
            setSnackbar({...snackbar, message:'All Devices Removed', severity:"success", open:true})

        })
    }

    const saveConfig = () => {
        let msg = 'Save Config, Not Yet Implemented'
        setSnackbar({...snackbar, message:msg, severity:"error", open:true})

    }

    useEffect(() => {
        getDeviceMetaDataCallback()
    }, []);

    return (
        <Paper elevation={1}>
            <Grid container spacing={1}>
                <Grid xs={1}>
                    <IconButton sx={{'& svg': {fontSize: 30}}}  onClick={deleteAllDevicesCall} aria-label="delete">
                        <DeleteIcon /> All
                    </IconButton>
                    <IconButton  sx={{'& svg': {fontSize: 30}}}  onClick={saveConfig} aria-label="refresh">
                        <SaveIcon/>
                    </IconButton>
                </Grid>              
                <Grid xs={11}>
                    <Accordion expanded={createDevice}
                        sx={{ ".MuiAccordionSummary-root": { "&:hover": { backgroundColor: '#d3d3d3' } } }}
                        onChange={createDeviceChange}
                    >
                        <AccordionSummary
                            expandIcon={<ExpandMoreIcon />}
                            aria-controls="panel1a-content"
                            id="panel1a-header"
                        >
                            <Typography variant="h4" marginLeft="35%">
                                <AddCircleIcon />
                                Create New Devices</Typography>
                        </AccordionSummary>
                        <AccordionDetails>
                            <CreateDevice getDeviceMetaDataCallback={getDeviceMetaDataCallback}></CreateDevice>
                        </AccordionDetails>
                    </Accordion>
                </Grid>

                {deviceMetaData.map((metadata, index) => (
                    <Grid key={index} xs={6} md={4}>
                        <DeviceCard key={metadata.device_id} device={metadata}>
                        </DeviceCard>
                    </Grid>
                )
                )}
            </Grid>
        </Paper>
    )

}

export default DevicePage;