import Grid from '@mui/material/Unstable_Grid2';
import Paper from '@mui/material/Paper';


import { useState, useEffect, useCallback } from 'react';
import DeviceCard from '../DeviceCard/DeviceCard'
import { getDevicesMetaData } from '../../Api/devives'

import Accordion from '@mui/material/Accordion';
import AccordionDetails from '@mui/material/AccordionDetails';
import AccordionSummary from '@mui/material/AccordionSummary';
import Typography from '@mui/material/Typography';

import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import AddCircleIcon from '@mui/icons-material/AddCircle';

import CreateDevice from '../CreateDevice/CreateDevice'

const DevicePage = () => {

    let number_cards = Array.from({ length: 5 }, (_, i) => i)

    const [deviceMetaData, setDeviceMetaData] = useState([]);
    const [createDevice, setCreateDevice] = useState(false);

    const createDeviceChange = () => {
        setCreateDevice(!createDevice);
    };

    useEffect(() => {
        getDevicesMetaData()
            .then((deviceMetaData) => {
                console.log(deviceMetaData);
                setDeviceMetaData(deviceMetaData)
            })
    }, []);

    return (
        <Paper elevation={1}>
            <Grid container spacing={1}>
                <Grid xs={12}>
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
                                Create New Device</Typography>
                        </AccordionSummary>
                        <AccordionDetails>
                            <CreateDevice></CreateDevice>
                        </AccordionDetails>
                    </Accordion>
                </Grid>

                {deviceMetaData.map((metadata, index) => (
                    <Grid key={index} xs={6} md={4}>
                        <DeviceCard key={metadata.device_id.toString()} device={metadata}>
                        </DeviceCard>
                    </Grid>
                )
                )}
            </Grid>
        </Paper>
    )

}

export default DevicePage;