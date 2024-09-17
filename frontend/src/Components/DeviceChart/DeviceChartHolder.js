import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import { Fragment, useState } from 'react';
import DeviceLineChart from './DeviceLineChart';
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";

function TabPanel(props) {
    const { children, value, index, ...other } = props;

    return (
        <div
            role="tabpanel"
            hidden={value !== index}
            id={`simple-tabpanel-${index}`}
            aria-labelledby={`simple-tab-${index}`}
            {...other}
        >
            {value === index && (
                <Box sx={{ marginTop: 2 }}>
                    {children}
                </Box>
            )}
        </div>
    );
}

const DeviceChartHolder = (props) => {

    const tabComponentGenerator = (deviceData, deviceMeta) => {
        let Components = [];
        let metrics = Object.keys(deviceData)


        for (let i = 0; i < metrics.length; i++) {

            let metric = metrics[i]

            let metric_attribute = deviceMeta.attributes.filter(device => device.name === metric)

            Components.push(
                {
                    'metric': metric,
                    'Component':
                        <Fragment>
                            <DeviceLineChart deviceData={deviceData[metric]} deviceMetric={metric} />
                            <Typography>Sampling : {metric_attribute[0].model.str_format} </Typography>
                        </Fragment>
                }
            )
        }
        return Components
    }

    const [tabValue, setTab] = useState(0);

    const handleChange = (event, newValue) => {
        setTab(newValue);
    };

    let deviceData = props.deviceData
    let deviceMeta = props.deviceMeta
    let tabComponents = tabComponentGenerator(deviceData, deviceMeta)

    return (
        <Fragment>
            <Tabs value={tabValue} onChange={handleChange} aria-label="Metrics">
                {tabComponents.map(({ metric }, index) => (
                    <Tab key={index} label={metric} />
                ))}
            </Tabs>
            {tabComponents.map(({ Component }, index) => (
                <TabPanel value={tabValue} index={index} key={index}>
                    <Fragment>
                        {Component}
                    </Fragment>
                </TabPanel>
            ))}
        </Fragment>
    );

}

export default DeviceChartHolder
