import Grid from '@mui/material/Unstable_Grid2';
import { Fragment, useState, useEffect, useRef } from 'react';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import { CardHeader } from '@mui/material';

import Typography from '@mui/material/Typography';
import IconButton from '@mui/material/IconButton'
import Paper from '@mui/material/Paper';



import { getDeviceData, startDevice, pauseDevice } from '../../Api/devives';
import DeviceChartHolder from '../DeviceChart/DeviceChartHolder'

import PauseIcon from '@mui/icons-material/Pause';
import PlayArrowIcon from '@mui/icons-material/PlayArrow';
import DeleteIcon from '@mui/icons-material/Delete';



const DeviceCard = (props) => {

    let title = "Device ID : " + props.device.device_id

    const [deviceData, setDeviceData] = useState([]);
    const [justStarted, setJustStarted] = useState(true);
    const [deviceStatus, setDeviceStatus] = useState(props.device.running);
    const interval = useRef();



    const refreshDeviceData = () => {
        getDeviceData(props.device.device_id)
            .then((deviceData) => {
                setDeviceData(deviceData)
            })
    }

    const changeDeviceStatus = () => {
        if (deviceStatus == true) {
            pauseDevice(props.device.device_id).then(
                setDeviceStatus(!deviceStatus)
            ).catch((error) =>
                console.log(error)
            )
        } else {
            startDevice(props.device.device_id).then(
                setDeviceStatus(!deviceStatus)
            ).catch((error) =>
                console.log(error)
            )
        }

    }

    useEffect(() => {

        return () => {
            console.log('Unmount Device Card')
            clearInterval(interval.current)
        };

    },[])

    useEffect(() => {
        clearInterval(interval.current);
        if(justStarted===true){
            refreshDeviceData()
            setJustStarted(false)
        }


        if (deviceStatus === true) {
            interval.current = setInterval(() => {
                refreshDeviceData()
                if (deviceStatus === false) {
                    clearInterval(interval)
                }
            }, props.device.delay * 1000)
        }
    }, [deviceStatus])



    return (
        <Paper elevation={2} sx={deviceStatus ? { 'backgroundColor': '#FFF' } : { 'backgroundColor': '#FFCCCB' }}>
            <CardHeader
                action={
                    <Fragment>
                        {deviceStatus ? (
                            <IconButton onClick={changeDeviceStatus} aria-label="settings">
                                <PauseIcon />
                            </IconButton>
                        ) :
                            <IconButton onClick={changeDeviceStatus} aria-label="settings">
                                <PlayArrowIcon />
                            </IconButton>
                        }
                        <IconButton aria-label="settings">
                            <DeleteIcon />
                        </IconButton>
                    </Fragment>

                }
                title={title}
                sx={{paddingBottom:'0px', paddingTop:'3px'}}
                >

            </CardHeader>
            <CardContent>
                <Grid container spacing={1}>
                    <Grid xs={12}>
                        <Typography variant="body2">
                            Reading Epoch : {props.device.delay} Second(s)
                        </Typography>
                    </Grid>
                    {Object.entries(props.device.meta_data).map(row => (
                        <Fragment key={row[0]}>
                            <Grid xs={12}>
                                <Typography variant="body2">
                                    {row[0]} : {row[1]}
                                </Typography>
                            </Grid>
                        </Fragment>
                    ))}
                </Grid>
                <Grid container>
                    <Grid xs={12}>
                        <DeviceChartHolder deviceData={deviceData} deviceMeta={props.device}></DeviceChartHolder>
                    </Grid>
                </Grid>

            </CardContent>
            <CardActions>
            </CardActions>
        </Paper>
    )

}

export default DeviceCard;