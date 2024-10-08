import { Fragment, useState, useContext, useEffect } from 'react';
import TextField from "@mui/material/TextField";

import Button from "@mui/material//Button";

import MenuItem from '@mui/material/MenuItem';
import Select from '@mui/material/Select';

import IconButton from '@mui/material/IconButton'
import DeleteIcon from "@mui/icons-material/Delete";

import Box from "@mui/material/Box";
import Grid from '@mui/material/Unstable_Grid2';

import Accordion from '@mui/material/Accordion';
import AccordionSummary from '@mui/material/AccordionSummary';
import AccordionDetails from '@mui/material/AccordionDetails';
import Typography from '@mui/material/Typography';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';

import FormHelperText from '@mui/material/FormHelperText';

import { DISTRIBUTIONS } from '../../Constants/distributions';
import {SnackbarContext} from "../../Contexts/SnackBarAlertContext";
import { createDevice } from '../../Api/devives';
import {getEndpoints} from '../../Api/endpoints';

import CreateEndpointDialog from '../CreateEndpoint/CreateEndpoint';


const CreateDevice = (props) => {

    const metaDataRow = { "key": "Location", "value": "Leeds" }
    const [metaData, setMetaData] = useState([metaDataRow]);

    const attributeRow = { "model": "Normal", "name": "Flow", 'sd':1, 'mean':10, 'beta_a':1, 'beta_b':2, 'scale':10}
    const [attributes, setAttributes] = useState([attributeRow]);

    const defaultProperties = { "delay": 10, "numberDevices": 1, "start": true, 'endpoint': 1 }
    const [properties, setProperties] = useState(defaultProperties);

    const [openCreateEndpoint, setOpenCreateEndpoint] = useState(false);

    const defaultEndpoint = {'name':'None', 'id':1, 'connection_string':''}
    const [endpoints, setEndpoints] = useState([defaultEndpoint]);

    const {snackbar, setSnackbar} = useContext(SnackbarContext);

    // HELPER
    const removeByIndex = (obj, index) => {
        let deepcopy_obj = JSON.parse(JSON.stringify(obj));
        return deepcopy_obj.splice(1, index)
    }

    const isNumeric = (val) => {
        return !isNaN(parseFloat(val)) && isFinite(val);
    }

    // ENDPOINTS

    const getEndpointsCall = () => {
        getEndpoints()
        .then((endpointData) => {
            setEndpoints(endpointData)
        })
    }

    useEffect(() => {
        getEndpointsCall()
    },[])

    // META DATA
    const handleMetaValueChange = (key, index, e) => {
        let newData = JSON.parse(JSON.stringify(metaData));
        newData[index][key] = e.target.value
        setMetaData(newData)
    }

    const deleteMetaValue = (index) => {
        let modifiedMetaData = removeByIndex(metaData, index)
        setMetaData(modifiedMetaData)
    };

    const addMetaDataRow = () => {
        setMetaData([...metaData, metaDataRow]);
    };

    // Attributions
    const handleAttributeChange = (key, index, e) => {
        let newData = JSON.parse(JSON.stringify(attributes));
        newData[index][key] = e.target.value
        setAttributes(newData)
    }

    const deleteAttibute = (index) => {
        let modifiedAttributes = removeByIndex(attributes, index)
        setAttributes(modifiedAttributes)
    };

    const addAttributeRow = () => {
        setAttributes([...attributes, attributeRow]);
    };

    // PROPERTIES
    const handlepropertiesChange = (key, e) => {
        let newData = JSON.parse(JSON.stringify(properties));
        newData[key] = e.target.value
        setProperties(newData)
    }

    // ACTIONS
    const resetCreateDevice = () => {
        setMetaData([metaDataRow])
        setAttributes([attributeRow])
        setProperties(defaultProperties)
        return
    }

    const createDevices = async() => {
        let propertErrors = checkValidPropertiesData(properties)
        let metaDataErrors = checkValidMetaData(metaData)
        let attributeErrors = checkValidAttributesData(attributes);

        let validationErrors = [...propertErrors, ...metaDataErrors, ...attributeErrors]

        if(validationErrors.length>0){
            let msg = validationErrors.join(' & ')
            setSnackbar({...snackbar, message:msg, severity:"error", open:true})
            return
        }

        let devicePostData = {
            "delay": properties.delay,
            "endpoint": properties.endpoint,
            'number_devices': properties.numberDevices,
            "start_instantly":true,
            "meta_data": metaData,
            "attributes": attributes            
        }

        let response = await createDevice(devicePostData).then(response => response)
        if(response.status < 200 || response.status>300){
            let msg = `Failed Creation of Device, Error Code ${response.status}, msg: ${response.statusText}`
            setSnackbar({...snackbar, message:msg, severity:"error", open:true})
            return 
        }
        setSnackbar({...snackbar, message:'Device Created', severity:"success", open:true})
        
        // Need time to wait for devices to turn on, couldn't be arsed writing code to check all new created devices turned on
        await new Promise(r => setTimeout(r, 500));

        props.getDeviceMetaDataCallback()
        resetCreateDevice();

    }

    const checkValidPropertiesData = (properties) => {
        let errors = [];

        if (!isNumeric(properties.delay)) {
            errors.push(['Propertes : delay must be of type number'])
        }

        if (properties.delay < 1){
            errors.push(['Propertes : delay has to be gte 1'])
        }

        if (!isNumeric(properties.numberDevices)) {
            errors.push(['Propertes : number devices must be of type number'])
        }

        if (properties.numberDevices < 1 || properties.numberDevices > 100 ){
            errors.push(['Propertes : number devices must be between 1 and 100'])
        }
        
        return errors
    }

    const checkValidAttributesData = (attributes) => {
        let errors = []
        
        attributes.map(a => { 
            if(a.name===''){
                errors.push('Attributes name must not be blank')
            }
            if(a.model==='Normal'){
                if(!isNumeric(a.mean)){
                    errors.push('Attributes Normal dist mean must be numeric')
                }
                if(!isNumeric(a.sd)){
                    errors.push('Attributes Normal dist standard dev must be numeric')
                }
                if(a.sd < 0){
                    errors.push('Attributes Normal dist Standard deviation must be gte 0')
                }
            }
            if(a.model==='Beta'){
                if(!isNumeric(a.beta_a)){
                    errors.push('Attributes beta model alpha must be numeric')
                }

                if(a.beta_a <= 0 || a.beta_a > 100){
                    errors.push('Attributes beta model alpha must be between 0 and 100')
                }

                if(!isNumeric(a.beta_b)){
                    errors.push('Attributes beta model beta must be numeric')
                }

                if(a.beta_b <= 0 || a.beta_b > 100){
                    errors.push('Attributes beta model beta must be between 0 and 100')
                }

                if(!isNumeric(a.scale)){
                    errors.push('Attributes beta model scale must be numeric')
                }

                if(a.scale <= 0 || a.scale > 100){
                    errors.push('Attributes beta model scale must be between 0 and 100')
                }
            }
        })
        return errors
    }

    const checkValidMetaData = (metaData) => {
        let errors = [];
        metaData.map(({key, value}) => {
            if(key==='' || value===''){
                errors.push(`MetaData key: ${key} and value: ${value} must both be not blank`)
            }
        })
        return errors
    }

    return (
        <Box
            component="form"
            sx={{
                '& .MuiTextField-root': { m: 1, width: '90%' },
            }}
        >
            <Grid container spacing={0}>
                <Grid xs={12} sm={12} md={3} lg={2} xl={2} >
                    <Typography sx={{ marginLeft: '30%' }} variant='subtitle1'>Properties</Typography>
                    <Grid container>
                        <Grid xs={10}>
                            <TextField
                                type='number'           
                                size="small"
                                autoFocus
                                margin="dense"
                                label="Number of devices"
                                value={properties.numberDevices}
                                onChange={(e) => handlepropertiesChange("numberDevices", e)}
                            />
                        </Grid>
                        <Grid xs={10}>
                            <TextField
                                type='number'
                                size="small"
                                autoFocus
                                margin="dense"
                                label="Reading epoch seconds"
                                value={properties.delay}
                                onChange={(e) => handlepropertiesChange("delay", e)}
                            />
                        </Grid>
                        <Grid xs={10}>
                            <Select
                                sx={{ minWidth: '40%', maxWidth: '77%',  marginLeft: '4%' }}
                                size="small"
                                labelId="Endpoint"
                                id={"Endpoint"}
                                value={properties.endpoint}
                                label="Endpoint"
                                onChange={(e) => handlepropertiesChange("endpoint", e)}
                            >
                                {endpoints.map((e, i) => (
                                    <MenuItem key={'endpoint'+i} value={e.id}>{e.name}</MenuItem>
                                ))}
                            </Select>
                            <CreateEndpointDialog 
                                openCreateEndpoint={openCreateEndpoint} 
                                setOpenCreateEndpoint={setOpenCreateEndpoint}
                                getEndpointsCall={getEndpointsCall}>
                            </CreateEndpointDialog>
                            <FormHelperText sx={{ marginLeft: '6%' }}>Configured Endpoint</FormHelperText>
                        </Grid>
                    </Grid>
                </Grid>

                <Grid xs={12} sm={12} md={4} lg={3} xl={3} >
                    <Typography sx={{ marginLeft: '30%' }} variant='subtitle1'>MetaData</Typography>
                    <Grid container spacing={0}>
                        {metaData.map((item, index) => (
                            <Fragment key={"meta" + index}>
                                <Grid xs={5}>
                                    <TextField
                                        size="small"
                                        autoFocus
                                        margin="dense"
                                        label="Label Name"
                                        value={item.key}
                                        sx={{ width: '350px' }}
                                        onChange={(e) => handleMetaValueChange("key", index, e)}
                                    />
                                </Grid>
                                <Grid xs={5}>
                                    <TextField
                                        size="small"
                                        autoFocus
                                        margin="dense"
                                        label="Value"
                                        value={item.value}
                                        sx={{ width: 350 }}
                                        onChange={(e) => handleMetaValueChange("value", index, e)}
                                    />
                                </Grid>
                                <Grid xs={1}>
                                    <IconButton sx={{ marginTop: '10%' }} onClick={() => deleteMetaValue(index)} aria-label="delete">
                                        <DeleteIcon />
                                    </IconButton>
                                </Grid>
                            </Fragment>
                        ))}
                        <Grid xs={12}>
                            <Button onClick={addMetaDataRow} color="primary">
                                Add
                            </Button>
                        </Grid>
                    </Grid>
                </Grid>

                <Grid item xs={12} sm={12} md={6} lg={6} xl={6} >
                    <Typography sx={{ marginLeft: '30%' }} variant='subtitle1'>Attributes</Typography>

                    <Grid container spacing={0} >
                        {attributes.map((item, index) => (
                            <Fragment key={'attribute' + index} >
                                <Grid xs={3} sm={3} md={3} lg={3} xl={3}>
                                    <Box>
                                        <TextField
                                            size="small"
                                            autoFocus
                                            margin="dense"
                                            label="Attribute Name"
                                            value={item.name}
                                            onChange={(e) => handleAttributeChange("name", index, e)}
                                            fullWidth
                                        />
                                    </Box>
                                </Grid>
                                <Grid xs={2}>
                                    <Select
                                        sx={{ minWidth: '100%', marginTop: '5%' }}
                                        size="small"
                                        labelId="distribution"
                                        id={"distribution" + index}
                                        value={item.model}
                                        onChange={(e) => handleAttributeChange('model', index, e)}
                                        label="Distribution"
                                    >

                                        {DISTRIBUTIONS.map(d => (
                                            <MenuItem key={'dist' + index + d} value={d}>{d}</MenuItem>
                                        ))}
                                    </Select>
                                </Grid>

                                {attributes[index]['model'] === 'Normal' ?
                                    <Fragment>
                                        <Grid xs={2}>
                                            <TextField
                                                type='number'
                                                size="small"
                                                autoFocus
                                                margin="dense"
                                                label="Mean"
                                                value={item.mean}
                                                onChange={(e) => handleAttributeChange("mean", index, e)}
                                                fullWidth
                                            />
                                        </Grid>
                                        <Grid xs={2}>
                                            <TextField
                                                type='number'
                                                size="small"
                                                autoFocus
                                                margin="dense"
                                                label="Standard Deviation"
                                                value={item.sd}
                                                onChange={(e) => handleAttributeChange("sd", index, e)}
                                                fullWidth
                                            />
                                        </Grid>
                                        <Grid xs={2}>
                                        </Grid>
                                        <Grid xs={1}>
                                            <IconButton sx={{ marginTop: '10%' }} onClick={() => deleteAttibute(index)} aria-label="delete">
                                                <DeleteIcon />
                                            </IconButton>
                                        </Grid>

                                    </Fragment>
                                    : attributes[index]['model'] === 'Beta' ?
                                        <Fragment>
                                            <Grid xs={2}>
                                                <TextField
                                                    type='number'
                                                    size="small"
                                                    autoFocus
                                                    margin="dense"
                                                    label="Alpha"
                                                    value={item.beta_a}
                                                    onChange={(e) => handleAttributeChange("beta_a", index, e)}
                                                    fullWidth
                                                />
                                            </Grid>
                                            <Grid xs={2}>
                                                <TextField
                                                    type='number'                                                    
                                                    size="small"
                                                    autoFocus
                                                    margin="dense"
                                                    label="Beta"
                                                    value={item.beta_b}
                                                    onChange={(e) => handleAttributeChange("beta_b", index, e)}
                                                    fullWidth
                                                />
                                            </Grid>
                                            <Grid xs={2}>
                                                <TextField
                                                    type='number'
                                                    size="small"
                                                    autoFocus
                                                    margin="dense"
                                                    label="Scale"
                                                    value={item.scale}
                                                    onChange={(e) => handleAttributeChange("scale", index, e)}
                                                    fullWidth
                                                />
                                            </Grid>
                                            <Grid xs={1}>
                                                <IconButton sx={{ marginTop: '10%' }} onClick={() => deleteAttibute(index)} aria-label="delete">
                                                    <DeleteIcon />
                                                </IconButton>
                                            </Grid>

                                        </Fragment>
                                        :
                                        <Grid xs={6}>
                                        </Grid>
                                }

                            </Fragment>
                        ))}
                        <Grid xs={12}>
                            <Button onClick={addAttributeRow} color="primary">
                                Add
                            </Button>
                        </Grid>
                    </Grid>
                </Grid>

                <Grid xs={12}>
                    <Grid container>
                        <Grid xs={9}>
                            <Accordion elevation={0} sx={{border: 0, borderColor: 'primary.white'}}>
                                <AccordionSummary
                                aria-controls="panel1a-content"
                                id="panel1a-header"
                                >
                                <Typography sx={{color:"#1978D2", }}>Advanced Options</Typography>
                                <ExpandMoreIcon />
                                </AccordionSummary>
                                <AccordionDetails>
                                <Typography>
                                    NOT IMPLEMENTED OPTIONS
                                </Typography>
                                </AccordionDetails>
                            </Accordion>
                        </Grid>
                        <Grid xs={1}>
                        </Grid>
                        <Grid xs={2}>
                            <Button onClick={createDevices} sx={{ marginRight: '10px' }} variant="contained">
                                Save
                            </Button>
                            <Button onClick={resetCreateDevice} variant="contained" color="error">
                                Reset
                            </Button>
                        </Grid>
                    </Grid>
                </Grid>
            </Grid>
        </Box>
    )
}

export default CreateDevice