import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogTitle from '@mui/material/DialogTitle';
import Grid from '@mui/material/Unstable_Grid2';

import IconButton from '@mui/material/IconButton'
import AddIcon from "@mui/icons-material/Add";

import { Fragment, useState, useContext } from 'react';

import MenuItem from '@mui/material/MenuItem';
import Select from '@mui/material/Select';

import {createEndpoint} from '../../Api/endpoints';
import {SnackbarContext} from "../../Contexts/SnackBarAlertContext";

const CreateEndpointDialog = (props) => {

    const openCreateEndpoint = props.openCreateEndpoint
    const setOpenCreateEndpoint = props.setOpenCreateEndpoint

    const defaultEndpoint = {'name':'', 'connection_string':'', 'eventhub_name':'', 'endpoint_type':'EventHub'}

    const [endpoint, setEndpoint] = useState(defaultEndpoint);
    const {snackbar, setSnackbar} = useContext(SnackbarContext);


    const handleClickOpen = () => {
        setOpenCreateEndpoint(true);
    };

    const handleClose = () => {
        setOpenCreateEndpoint(false);
    };

    const handleEndpointChange = (key, e) => {
        let deepcopyEndpoint = JSON.parse(JSON.stringify(endpoint));
        deepcopyEndpoint[key] = e.target.value
        setEndpoint(deepcopyEndpoint)
    };

    const saveEndpoint = () => {
        let endpointErrors = validateEndpoint(endpoint)
        if(endpointErrors.length>0){
            let msg = endpointErrors.join(' & ')
            setSnackbar({...snackbar, message:msg, severity:"error", open:true})
            return
        }

        let response = createEndpoint(endpoint).then(response => response)
        if(response.status < 200 || response.status>300){
            let msg = `Failed in creating endpoint, Error Code ${response.status}, msg: ${response.statusText}`
            setSnackbar({...snackbar, message:msg, severity:"error", open:true})
            return 
        }
        props.getEndpointsCall()
        let msg = `Endpoint ${endpoint.name} Created`
        setSnackbar({...snackbar, message:msg, severity:"success", open:true})    
        setEndpoint(defaultEndpoint)
        setOpenCreateEndpoint(false)
    
    };

    const validateEndpoint = (endpoint) => {
        let errors = []
        
        if(endpoint.name===''){
            errors.push('Name Can not be blank')
        }
        if(endpoint.endpoint_type==='EventHub'){
            if(endpoint.connection_string===''){
                errors.push('Connection String can not be blank')
            }
        }

        return errors
    }

    return (
        <Fragment>
            <IconButton aria-label="add endpoint"  onClick={handleClickOpen}>
            <AddIcon />
            </IconButton>
            <Dialog open={openCreateEndpoint} onClose={handleClose}>
            <DialogTitle>Create Endpoint</DialogTitle>
            <DialogContent>
                <Grid container>
                    <Grid xs={12}>
                        <Select
                            size="small"
                            labelId="Endpoint"
                            id={"Endpoint"}
                            value={endpoint.endpoint_type}
                            label="Endpoint"
                            onChange={(e) => handleEndpointChange('endpoint_type', e)}
                        >
                            <MenuItem value={'EventHub'}>EventHub</MenuItem>
                            <MenuItem value={'Kafka'}>Kafka</MenuItem>

                        </Select>
                    </Grid>
                    <Grid xs={12}>
                        <TextField
                            autoFocus
                            margin="dense"
                            id="name"
                            value={endpoint.name}
                            onChange={(e) => handleEndpointChange('name', e)}
                            label="Name"
                            fullWidth
                            variant="standard"
                        />
                    </Grid>

                    {endpoint.endpoint_type==='EventHub' ?
                        <Fragment>
                            <Grid xs={12}>
                                <TextField
                                    autoFocus
                                    margin="dense"
                                    id="ConnectionStringEventHub"
                                    label="ConnectionString"
                                    value={endpoint.connection_string}
                                    onChange={(e) => handleEndpointChange('connection_string', e)}
                                    fullWidth
                                    variant="standard"
                                />
                            </Grid>
                            <Grid xs={12}>
                                <TextField
                                    autoFocus
                                    margin="dense"
                                    id="EventHubName"
                                    label="EventHub Name"
                                    value={endpoint.eventhub_name}
                                    onChange={(e) => handleEndpointChange('eventhub_name', e)}
                                    fullWidth
                                    variant="standard"
                                />
                            </Grid>
                        </Fragment>
                        
                    :
                    <Grid xs={12}>
                        <div><b>NOT IMPLEMENTED</b></div>
                    </Grid>
                    }

                </Grid>
            </DialogContent>
            <DialogActions>
                <Button onClick={handleClose}>Cancel</Button>
                <Button onClick={saveEndpoint}>Save</Button>
            </DialogActions>
            </Dialog>
        </Fragment>
    );
}

    export default CreateEndpointDialog;