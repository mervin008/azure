import time
from google.cloud import monitoring_v3

project_id = "your-gcp-project-id"  # Replace with your project ID
client = monitoring_v3.MetricServiceClient()
project_name = client.common_project_path(project_id)

# Metric definitions
total_requests_metric = monitoring_v3.MetricDescriptor()
total_requests_metric.type = "custom.googleapis.com/certhub_email_requests_total"
total_requests_metric.metric_kind = monitoring_v3.MetricDescriptor.MetricKind.CUMULATIVE
total_requests_metric.value_type = monitoring_v3.MetricDescriptor.ValueType.INT64

user_emails_metric = monitoring_v3.MetricDescriptor()
user_emails_metric.type = "custom.googleapis.com/certhub_user_emails_total"
user_emails_metric.metric_kind = monitoring_v3.MetricDescriptor.MetricKind.CUMULATIVE
user_emails_metric.value_type = monitoring_v3.MetricDescriptor.ValueType.INT64

team_emails_metric = monitoring_v3.MetricDescriptor()
team_emails_metric.type = "custom.googleapis.com/certhub_team_emails_total"
team_emails_metric.metric_kind = monitoring_v3.MetricDescriptor.MetricKind.CUMULATIVE
team_emails_metric.value_type = monitoring_v3.MetricDescriptor.ValueType.INT64

combined_failures_metric = monitoring_v3.MetricDescriptor()
combined_failures_metric.type = "custom.googleapis.com/certhub_failures_total"
combined_failures_metric.metric_kind = monitoring_v3.MetricDescriptor.MetricKind.CUMULATIVE
combined_failures_metric.value_type = monitoring_v3.MetricDescriptor.ValueType.INT64

template_metrics = {}  

def create_metric_descriptor(metric_type):
    descriptor = monitoring_v3.MetricDescriptor()
    descriptor.type = metric_type
    descriptor.metric_kind = monitoring_v3.MetricDescriptor.MetricKind.CUMULATIVE
    descriptor.value_type = monitoring_v3.MetricDescriptor.ValueType.INT64
    return descriptor

def report_metric(metric_descriptor, value):     
    metric = monitoring_v3.types.Metric()
    metric.type = metric_descriptor.type
    resource = monitoring_v3.types.MonitoredResource(type='global') 

    point = monitoring_v3.types.Point()
    point.interval.end_time.seconds = int(time.time())
    point.value.int64_value = value
    metric.points.append(point)

    timeseries = monitoring_v3.types.TimeSeries()
    timeseries.metric = metric
    timeseries.resource = resource
    client.create_time_series(name=project_name, time_series=[timeseries])

def track_user_email(template_name):
    report_metric(user_emails_metric, 1) 
    track_template_usage(template_name)

def track_team_email(template_name):
    report_metric(team_emails_metric, 1) 
    track_template_usage(template_name)

def track_template_usage(template_name):
    if template_name not in template_metrics:
        metric_type = f"custom.googleapis.com/certhub_template_{template_name}_sent"
        template_metrics[template_name] = create_metric_descriptor(metric_type)  
    report_metric(template_metrics[template_name], 1) 

def report_failure(): 
    report_metric(combined_failures_metric, 1)
