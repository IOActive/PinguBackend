# Snippets API

> Version v1

Path Table

| Method | Path                                            | Description |
| ------ | ----------------------------------------------- | ----------- |
| POST   | [/api-token-auth/](#postapi-token-auth)            |             |
| POST   | [/auth/login/](#postauthlogin)                     |             |
| POST   | [/auth/refresh/](#postauthrefresh)                 |             |
| POST   | [/auth/register/](#postauthregister)               |             |
| GET    | [/bot/](#getbot)                                   |             |
| POST   | [/bot/](#postbot)                                  |             |
| PATCH  | [/bot/{id}/](#patchbotid)                          |             |
| DELETE | [/bot/{id}/](#deletebotid)                         |             |
| GET    | [/buildmetadata/](#getbuildmetadata)               |             |
| POST   | [/buildmetadata/](#postbuildmetadata)              |             |
| PATCH  | [/buildmetadata/{id}/](#patchbuildmetadataid)      |             |
| DELETE | [/buildmetadata/{id}/](#deletebuildmetadataid)     |             |
| GET    | [/coverage/](#getcoverage)                         |             |
| POST   | [/coverage/](#postcoverage)                        |             |
| PATCH  | [/coverage/{id}/](#patchcoverageid)                |             |
| DELETE | [/coverage/{id}/](#deletecoverageid)               |             |
| GET    | [/crash/](#getcrash)                               |             |
| POST   | [/crash/](#postcrash)                              |             |
| PATCH  | [/crash/{id}/](#patchcrashid)                      |             |
| DELETE | [/crash/{id}/](#deletecrashid)                     |             |
| GET    | [/databundle/](#getdatabundle)                     |             |
| POST   | [/databundle/](#postdatabundle)                    |             |
| PATCH  | [/databundle/{id}/](#patchdatabundleid)            |             |
| DELETE | [/databundle/{id}/](#deletedatabundleid)           |             |
| GET    | [/fuzzer/](#getfuzzer)                             |             |
| POST   | [/fuzzer/](#postfuzzer)                            |             |
| PATCH  | [/fuzzer/{id}/](#patchfuzzerid)                    |             |
| DELETE | [/fuzzer/{id}/](#deletefuzzerid)                   |             |
| GET    | [/fuzztarget/](#getfuzztarget)                     |             |
| POST   | [/fuzztarget/](#postfuzztarget)                    |             |
| PATCH  | [/fuzztarget/{id}/](#patchfuzztargetid)            |             |
| DELETE | [/fuzztarget/{id}/](#deletefuzztargetid)           |             |
| GET    | [/fuzztargetjob/](#getfuzztargetjob)               |             |
| POST   | [/fuzztargetjob/](#postfuzztargetjob)              |             |
| PATCH  | [/fuzztargetjob/{id}/](#patchfuzztargetjobid)      |             |
| DELETE | [/fuzztargetjob/{id}/](#deletefuzztargetjobid)     |             |
| GET    | [/job/](#getjob)                                   |             |
| POST   | [/job/](#postjob)                                  |             |
| PATCH  | [/job/{id}/](#patchjobid)                          |             |
| DELETE | [/job/{id}/](#deletejobid)                         |             |
| GET    | [/jobtemplate/](#getjobtemplate)                   |             |
| POST   | [/jobtemplate/](#postjobtemplate)                  |             |
| PATCH  | [/jobtemplate/{id}/](#patchjobtemplateid)          |             |
| DELETE | [/jobtemplate/{id}/](#deletejobtemplateid)         |             |
| GET    | [/stadistics/](#getstadistics)                     |             |
| POST   | [/stadistics/](#poststadistics)                    |             |
| PATCH  | [/stadistics/{id}/](#patchstadisticsid)            |             |
| DELETE | [/stadistics/{id}/](#deletestadisticsid)           |             |
| GET    | [/task/](#gettask)                                 |             |
| POST   | [/task/](#posttask)                                |             |
| GET    | [/testcase/](#gettestcase)                         |             |
| POST   | [/testcase/](#posttestcase)                        |             |
| PATCH  | [/testcase/{id}/](#patchtestcaseid)                |             |
| DELETE | [/testcase/{id}/](#deletetestcaseid)               |             |
| GET    | [/testcasevariant/](#gettestcasevariant)           |             |
| POST   | [/testcasevariant/](#posttestcasevariant)          |             |
| PATCH  | [/testcasevariant/{id}/](#patchtestcasevariantid)  |             |
| DELETE | [/testcasevariant/{id}/](#deletetestcasevariantid) |             |
| POST   | [/token/](#posttoken)                              |             |
| POST   | [/token/refresh/](#posttokenrefresh)               |             |
| GET    | [/trial/](#gettrial)                               |             |
| POST   | [/trial/](#posttrial)                              |             |
| PATCH  | [/trial/{id}/](#patchtrialid)                      |             |
| DELETE | [/trial/{id}/](#deletetrialid)                     |             |

## Reference Table

| Name            | Path                                                                               | Description |
| --------------- | ---------------------------------------------------------------------------------- | ----------- |
| FuzzTarget      | [#/components/requestBodies/FuzzTarget](#componentsrequestbodiesfuzztarget)           |             |
| BuildMetadata   | [#/components/requestBodies/BuildMetadata](#componentsrequestbodiesbuildmetadata)     |             |
| JobTemplate     | [#/components/requestBodies/JobTemplate](#componentsrequestbodiesjobtemplate)         |             |
| Bot             | [#/components/requestBodies/Bot](#componentsrequestbodiesbot)                         |             |
| TestCase        | [#/components/requestBodies/TestCase](#componentsrequestbodiestestcase)               |             |
| Coverage        | [#/components/requestBodies/Coverage](#componentsrequestbodiescoverage)               |             |
| TestCaseVariant | [#/components/requestBodies/TestCaseVariant](#componentsrequestbodiestestcasevariant) |             |
| FuzzTargetJob   | [#/components/requestBodies/FuzzTargetJob](#componentsrequestbodiesfuzztargetjob)     |             |
| TokenRefresh    | [#/components/requestBodies/TokenRefresh](#componentsrequestbodiestokenrefresh)       |             |
| Crash           | [#/components/requestBodies/Crash](#componentsrequestbodiescrash)                     |             |
| DataBundle      | [#/components/requestBodies/DataBundle](#componentsrequestbodiesdatabundle)           |             |
| Fuzzer          | [#/components/requestBodies/Fuzzer](#componentsrequestbodiesfuzzer)                   |             |
| Job             | [#/components/requestBodies/Job](#componentsrequestbodiesjob)                         |             |
| Statistic       | [#/components/requestBodies/Statistic](#componentsrequestbodiesstatistic)             |             |
| Trial           | [#/components/requestBodies/Trial](#componentsrequestbodiestrial)                     |             |
| Basic           | [#/components/securitySchemes/Basic](#componentssecurityschemesbasic)                 |             |
| AuthToken       | [#/components/schemas/AuthToken](#componentsschemasauthtoken)                         |             |
| Login           | [#/components/schemas/Login](#componentsschemaslogin)                                 |             |
| TokenRefresh    | [#/components/schemas/TokenRefresh](#componentsschemastokenrefresh)                   |             |
| Register        | [#/components/schemas/Register](#componentsschemasregister)                           |             |
| Bot             | [#/components/schemas/Bot](#componentsschemasbot)                                     |             |
| BuildMetadata   | [#/components/schemas/BuildMetadata](#componentsschemasbuildmetadata)                 |             |
| Coverage        | [#/components/schemas/Coverage](#componentsschemascoverage)                           |             |
| Crash           | [#/components/schemas/Crash](#componentsschemascrash)                                 |             |
| DataBundle      | [#/components/schemas/DataBundle](#componentsschemasdatabundle)                       |             |
| Fuzzer          | [#/components/schemas/Fuzzer](#componentsschemasfuzzer)                               |             |
| FuzzTarget      | [#/components/schemas/FuzzTarget](#componentsschemasfuzztarget)                       |             |
| FuzzTargetJob   | [#/components/schemas/FuzzTargetJob](#componentsschemasfuzztargetjob)                 |             |
| Job             | [#/components/schemas/Job](#componentsschemasjob)                                     |             |
| JobTemplate     | [#/components/schemas/JobTemplate](#componentsschemasjobtemplate)                     |             |
| Statistic       | [#/components/schemas/Statistic](#componentsschemasstatistic)                         |             |
| TestCase        | [#/components/schemas/TestCase](#componentsschemastestcase)                           |             |
| TestCaseVariant | [#/components/schemas/TestCaseVariant](#componentsschemastestcasevariant)             |             |
| TokenObtainPair | [#/components/schemas/TokenObtainPair](#componentsschemastokenobtainpair)             |             |
| Trial           | [#/components/schemas/Trial](#componentsschemastrial)                                 |             |

## Path Details

---

### [POST]/api-token-auth/

#### RequestBody

- application/json

```ts
{
  username: string
  password: string
  token?: string
}
```

#### Responses

- 201

`application/json`

```ts
{
  username: string
  password: string
  token?: string
}
```

---

### [POST]/auth/login/

#### RequestBody

- application/json

```ts
{
  username: string
  password: string
}
```

#### Responses

- 201

`application/json`

```ts
{
  username: string
  password: string
}
```

---

### [POST]/auth/refresh/

#### RequestBody

- application/json

```ts
{
  refresh: string
  access?: string
}
```

#### Responses

- 201

`application/json`

```ts
{
  refresh: string
  access?: string
}
```

---

### [POST]/auth/register/

#### RequestBody

- application/json

```ts
{
  id?: integer
  // Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.
  username: string
  email: string
  password: string
  // Designates whether this user should be treated as active. Unselect this instead of deleting accounts.
  is_active?: boolean
}
```

#### Responses

- 201

`application/json`

```ts
{
  id?: integer
  // Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.
  username: string
  email: string
  password: string
  // Designates whether this user should be treated as active. Unselect this instead of deleting accounts.
  is_active?: boolean
}
```

---

### [GET]/bot/

#### Parameters(Query)

```ts
id?: string
```

```ts
name?: string
```

```ts
page?: integer
```

#### Responses

- 200

`application/json`

```ts
{
  count: integer
  next?: string
  previous?: string
  results: {
    id?: string
    name: string
    last_beat_time?: string
    task_payload?: string
    task_end_time?: string
    task_status?: enum[started, in-progress, finished, errored out, NA]
    platform?: enum[Android, Linux, Mac, Windows, NA]
    blobstore_log_path?: string
    bot_logs?: string
  }[]
}
```

---

### [POST]/bot/

#### RequestBody

- application/json

```ts
{
  id?: string
  name: string
  last_beat_time?: string
  task_payload?: string
  task_end_time?: string
  task_status?: enum[started, in-progress, finished, errored out, NA]
  platform?: enum[Android, Linux, Mac, Windows, NA]
  blobstore_log_path?: string
  bot_logs?: string
}
```

#### Responses

- 201

`application/json`

```ts
{
  id?: string
  name: string
  last_beat_time?: string
  task_payload?: string
  task_end_time?: string
  task_status?: enum[started, in-progress, finished, errored out, NA]
  platform?: enum[Android, Linux, Mac, Windows, NA]
  blobstore_log_path?: string
  bot_logs?: string
}
```

---

### [PATCH]/bot//

#### RequestBody

- application/json

```ts
{
  id?: string
  name: string
  last_beat_time?: string
  task_payload?: string
  task_end_time?: string
  task_status?: enum[started, in-progress, finished, errored out, NA]
  platform?: enum[Android, Linux, Mac, Windows, NA]
  blobstore_log_path?: string
  bot_logs?: string
}
```

#### Responses

- 200

`application/json`

```ts
{
  id?: string
  name: string
  last_beat_time?: string
  task_payload?: string
  task_end_time?: string
  task_status?: enum[started, in-progress, finished, errored out, NA]
  platform?: enum[Android, Linux, Mac, Windows, NA]
  blobstore_log_path?: string
  bot_logs?: string
}
```

---

### [DELETE]/bot//

#### Responses

- 204

---

### [GET]/buildmetadata/

#### Parameters(Query)

```ts
id?: string
```

```ts
job?: string
```

```ts
revision?: number
```

```ts
page?: integer
```

#### Responses

- 200

`application/json`

```ts
{
  count: integer
  next?: string
  previous?: string
  results: {
    id?: string
    job?: string
    revision?: integer
    bad_build?: boolean
    console_output?: string
    bot_name: string
    symbols?: string
    timestamp: string
  }[]
}
```

---

### [POST]/buildmetadata/

#### RequestBody

- application/json

```ts
{
  id?: string
  job?: string
  revision?: integer
  bad_build?: boolean
  console_output?: string
  bot_name: string
  symbols?: string
  timestamp: string
}
```

#### Responses

- 201

`application/json`

```ts
{
  id?: string
  job?: string
  revision?: integer
  bad_build?: boolean
  console_output?: string
  bot_name: string
  symbols?: string
  timestamp: string
}
```

---

### [PATCH]/buildmetadata//

#### RequestBody

- application/json

```ts
{
  id?: string
  job?: string
  revision?: integer
  bad_build?: boolean
  console_output?: string
  bot_name: string
  symbols?: string
  timestamp: string
}
```

#### Responses

- 200

`application/json`

```ts
{
  id?: string
  job?: string
  revision?: integer
  bad_build?: boolean
  console_output?: string
  bot_name: string
  symbols?: string
  timestamp: string
}
```

---

### [DELETE]/buildmetadata//

#### Responses

- 204

---

### [GET]/coverage/

#### Parameters(Query)

```ts
id?: string
```

```ts
page?: integer
```

#### Responses

- 200

`application/json`

```ts
{
  count: integer
  next?: string
  previous?: string
  results: {
    id?: string
    date: string
    fuzzer: string
    functions_covered: integer
    functions_total: integer
    edges_covered: integer
    edges_total: integer
    corpus_size_units: integer
    corpus_size_bytes: integer
    corpus_location: string
    corpus_backup_location: string
    quarantine_size_units: integer
    quarantine_size_bytes: integer
    quarantine_location: string
    html_report_url?: string
    testcase: string
  }[]
}
```

---

### [POST]/coverage/

#### RequestBody

- application/json

```ts
{
  id?: string
  date: string
  fuzzer: string
  functions_covered: integer
  functions_total: integer
  edges_covered: integer
  edges_total: integer
  corpus_size_units: integer
  corpus_size_bytes: integer
  corpus_location: string
  corpus_backup_location: string
  quarantine_size_units: integer
  quarantine_size_bytes: integer
  quarantine_location: string
  html_report_url?: string
  testcase: string
}
```

#### Responses

- 201

`application/json`

```ts
{
  id?: string
  date: string
  fuzzer: string
  functions_covered: integer
  functions_total: integer
  edges_covered: integer
  edges_total: integer
  corpus_size_units: integer
  corpus_size_bytes: integer
  corpus_location: string
  corpus_backup_location: string
  quarantine_size_units: integer
  quarantine_size_bytes: integer
  quarantine_location: string
  html_report_url?: string
  testcase: string
}
```

---

### [PATCH]/coverage//

#### RequestBody

- application/json

```ts
{
  id?: string
  date: string
  fuzzer: string
  functions_covered: integer
  functions_total: integer
  edges_covered: integer
  edges_total: integer
  corpus_size_units: integer
  corpus_size_bytes: integer
  corpus_location: string
  corpus_backup_location: string
  quarantine_size_units: integer
  quarantine_size_bytes: integer
  quarantine_location: string
  html_report_url?: string
  testcase: string
}
```

#### Responses

- 200

`application/json`

```ts
{
  id?: string
  date: string
  fuzzer: string
  functions_covered: integer
  functions_total: integer
  edges_covered: integer
  edges_total: integer
  corpus_size_units: integer
  corpus_size_bytes: integer
  corpus_location: string
  corpus_backup_location: string
  quarantine_size_units: integer
  quarantine_size_bytes: integer
  quarantine_location: string
  html_report_url?: string
  testcase: string
}
```

---

### [DELETE]/coverage//

#### Responses

- 204

---

### [GET]/crash/

#### Parameters(Query)

```ts
id?: string
```

```ts
testcase_id?: string
```

```ts
page?: integer
```

#### Responses

- 200

`application/json`

```ts
{
  count: integer
  next?: string
  previous?: string
  results: {
    id?: string
    testcase_id: string
    crash_signal: integer
    exploitability?: string
    crash_time: integer
    crash_hash: string
    verified?: boolean
    additional?: string
    iteration: integer
    crash_type: string
    crash_address?: string
    crash_state: string
    crash_stacktrace: string
    regression?: string
    security_severity?: integer
    absolute_path: string
    security_flag: boolean
    reproducible_flag?: boolean
    return_code: string
    gestures: {
    }
    resource_list: {
    }
    fuzzing_strategy: {
    }
    should_be_ignored?: boolean
    application_command_line?: string
    unsymbolized_crash_stacktrace: string
    crash_frame: {
    }
    crash_info?: string
    crash_revision?: integer
  }[]
}
```

---

### [POST]/crash/

#### RequestBody

- application/json

```ts
{
  id?: string
  testcase_id: string
  crash_signal: integer
  exploitability?: string
  crash_time: integer
  crash_hash: string
  verified?: boolean
  additional?: string
  iteration: integer
  crash_type: string
  crash_address?: string
  crash_state: string
  crash_stacktrace: string
  regression?: string
  security_severity?: integer
  absolute_path: string
  security_flag: boolean
  reproducible_flag?: boolean
  return_code: string
  gestures: {
  }
  resource_list: {
  }
  fuzzing_strategy: {
  }
  should_be_ignored?: boolean
  application_command_line?: string
  unsymbolized_crash_stacktrace: string
  crash_frame: {
  }
  crash_info?: string
  crash_revision?: integer
}
```

#### Responses

- 201

`application/json`

```ts
{
  id?: string
  testcase_id: string
  crash_signal: integer
  exploitability?: string
  crash_time: integer
  crash_hash: string
  verified?: boolean
  additional?: string
  iteration: integer
  crash_type: string
  crash_address?: string
  crash_state: string
  crash_stacktrace: string
  regression?: string
  security_severity?: integer
  absolute_path: string
  security_flag: boolean
  reproducible_flag?: boolean
  return_code: string
  gestures: {
  }
  resource_list: {
  }
  fuzzing_strategy: {
  }
  should_be_ignored?: boolean
  application_command_line?: string
  unsymbolized_crash_stacktrace: string
  crash_frame: {
  }
  crash_info?: string
  crash_revision?: integer
}
```

---

### [PATCH]/crash//

#### RequestBody

- application/json

```ts
{
  id?: string
  testcase_id: string
  crash_signal: integer
  exploitability?: string
  crash_time: integer
  crash_hash: string
  verified?: boolean
  additional?: string
  iteration: integer
  crash_type: string
  crash_address?: string
  crash_state: string
  crash_stacktrace: string
  regression?: string
  security_severity?: integer
  absolute_path: string
  security_flag: boolean
  reproducible_flag?: boolean
  return_code: string
  gestures: {
  }
  resource_list: {
  }
  fuzzing_strategy: {
  }
  should_be_ignored?: boolean
  application_command_line?: string
  unsymbolized_crash_stacktrace: string
  crash_frame: {
  }
  crash_info?: string
  crash_revision?: integer
}
```

#### Responses

- 200

`application/json`

```ts
{
  id?: string
  testcase_id: string
  crash_signal: integer
  exploitability?: string
  crash_time: integer
  crash_hash: string
  verified?: boolean
  additional?: string
  iteration: integer
  crash_type: string
  crash_address?: string
  crash_state: string
  crash_stacktrace: string
  regression?: string
  security_severity?: integer
  absolute_path: string
  security_flag: boolean
  reproducible_flag?: boolean
  return_code: string
  gestures: {
  }
  resource_list: {
  }
  fuzzing_strategy: {
  }
  should_be_ignored?: boolean
  application_command_line?: string
  unsymbolized_crash_stacktrace: string
  crash_frame: {
  }
  crash_info?: string
  crash_revision?: integer
}
```

---

### [DELETE]/crash//

#### Responses

- 204

---

### [GET]/databundle/

#### Parameters(Query)

```ts
id?: string
```

```ts
name?: string
```

```ts
page?: integer
```

#### Responses

- 200

`application/json`

```ts
{
  count: integer
  next?: string
  previous?: string
  results: {
    id?: string
    name: string
    bucket_name: string
    source?: string
    is_local?: boolean
    timestamp: string
    sync_to_worker?: boolean
  }[]
}
```

---

### [POST]/databundle/

#### RequestBody

- application/json

```ts
{
  id?: string
  name: string
  bucket_name: string
  source?: string
  is_local?: boolean
  timestamp: string
  sync_to_worker?: boolean
}
```

#### Responses

- 201

`application/json`

```ts
{
  id?: string
  name: string
  bucket_name: string
  source?: string
  is_local?: boolean
  timestamp: string
  sync_to_worker?: boolean
}
```

---

### [PATCH]/databundle//

#### RequestBody

- application/json

```ts
{
  id?: string
  name: string
  bucket_name: string
  source?: string
  is_local?: boolean
  timestamp: string
  sync_to_worker?: boolean
}
```

#### Responses

- 200

`application/json`

```ts
{
  id?: string
  name: string
  bucket_name: string
  source?: string
  is_local?: boolean
  timestamp: string
  sync_to_worker?: boolean
}
```

---

### [DELETE]/databundle//

#### Responses

- 204

---

### [GET]/fuzzer/

#### Parameters(Query)

```ts
id?: string
```

```ts
name?: string
```

```ts
page?: integer
```

#### Responses

- 200

`application/json`

```ts
{
  count: integer
  next?: string
  previous?: string
  results: {
    id?: string
    timestamp?: string
    name: string
    filename?: string
    file_size?: integer
    // Content of the file base64 encoded
    fuzzer_zip?: string
    blobstore_path?: string
    executable_path?: string
    revision?: number
    timeout?: integer
    supported_platforms?: enum[Android, Linux, Mac, Windows, NA]
    launcher_script?: string
    result?: string
    result_timestamp?: string
    console_output?: string
    return_code?: integer
    sample_testcase?: string
    max_testcases?: integer
    untrusted_content?: boolean
    additional_environment_string?: string
    stats_columns: {
    }
    stats_column_descriptions: {
    }
    builtin?: boolean
    differential?: boolean
    has_large_testcases?: boolean
    data_bundle_name?: string
  }[]
}
```

---

### [POST]/fuzzer/

#### RequestBody

- application/json

```ts
{
  id?: string
  timestamp?: string
  name: string
  filename?: string
  file_size?: integer
  // Content of the file base64 encoded
  fuzzer_zip?: string
  blobstore_path?: string
  executable_path?: string
  revision?: number
  timeout?: integer
  supported_platforms?: enum[Android, Linux, Mac, Windows, NA]
  launcher_script?: string
  result?: string
  result_timestamp?: string
  console_output?: string
  return_code?: integer
  sample_testcase?: string
  max_testcases?: integer
  untrusted_content?: boolean
  additional_environment_string?: string
  stats_columns: {
  }
  stats_column_descriptions: {
  }
  builtin?: boolean
  differential?: boolean
  has_large_testcases?: boolean
  data_bundle_name?: string
}
```

#### Responses

- 201

`application/json`

```ts
{
  id?: string
  timestamp?: string
  name: string
  filename?: string
  file_size?: integer
  // Content of the file base64 encoded
  fuzzer_zip?: string
  blobstore_path?: string
  executable_path?: string
  revision?: number
  timeout?: integer
  supported_platforms?: enum[Android, Linux, Mac, Windows, NA]
  launcher_script?: string
  result?: string
  result_timestamp?: string
  console_output?: string
  return_code?: integer
  sample_testcase?: string
  max_testcases?: integer
  untrusted_content?: boolean
  additional_environment_string?: string
  stats_columns: {
  }
  stats_column_descriptions: {
  }
  builtin?: boolean
  differential?: boolean
  has_large_testcases?: boolean
  data_bundle_name?: string
}
```

---

### [PATCH]/fuzzer//

#### RequestBody

- application/json

```ts
{
  id?: string
  timestamp?: string
  name: string
  filename?: string
  file_size?: integer
  // Content of the file base64 encoded
  fuzzer_zip?: string
  blobstore_path?: string
  executable_path?: string
  revision?: number
  timeout?: integer
  supported_platforms?: enum[Android, Linux, Mac, Windows, NA]
  launcher_script?: string
  result?: string
  result_timestamp?: string
  console_output?: string
  return_code?: integer
  sample_testcase?: string
  max_testcases?: integer
  untrusted_content?: boolean
  additional_environment_string?: string
  stats_columns: {
  }
  stats_column_descriptions: {
  }
  builtin?: boolean
  differential?: boolean
  has_large_testcases?: boolean
  data_bundle_name?: string
}
```

#### Responses

- 200

`application/json`

```ts
{
  id?: string
  timestamp?: string
  name: string
  filename?: string
  file_size?: integer
  // Content of the file base64 encoded
  fuzzer_zip?: string
  blobstore_path?: string
  executable_path?: string
  revision?: number
  timeout?: integer
  supported_platforms?: enum[Android, Linux, Mac, Windows, NA]
  launcher_script?: string
  result?: string
  result_timestamp?: string
  console_output?: string
  return_code?: integer
  sample_testcase?: string
  max_testcases?: integer
  untrusted_content?: boolean
  additional_environment_string?: string
  stats_columns: {
  }
  stats_column_descriptions: {
  }
  builtin?: boolean
  differential?: boolean
  has_large_testcases?: boolean
  data_bundle_name?: string
}
```

---

### [DELETE]/fuzzer//

#### Responses

- 204

---

### [GET]/fuzztarget/

#### Parameters(Query)

```ts
id?: string
```

```ts
fuzzer_engine?: string
```

```ts
binary?: string
```

```ts
page?: integer
```

#### Responses

- 200

`application/json`

```ts
{
  count: integer
  next?: string
  previous?: string
  results: {
    id?: string
    fuzzer_engine: string
    project: string
    binary: string
  }[]
}
```

---

### [POST]/fuzztarget/

#### RequestBody

- application/json

```ts
{
  id?: string
  fuzzer_engine: string
  project: string
  binary: string
}
```

#### Responses

- 201

`application/json`

```ts
{
  id?: string
  fuzzer_engine: string
  project: string
  binary: string
}
```

---

### [PATCH]/fuzztarget//

#### RequestBody

- application/json

```ts
{
  id?: string
  fuzzer_engine: string
  project: string
  binary: string
}
```

#### Responses

- 200

`application/json`

```ts
{
  id?: string
  fuzzer_engine: string
  project: string
  binary: string
}
```

---

### [DELETE]/fuzztarget//

#### Responses

- 204

---

### [GET]/fuzztargetjob/

#### Parameters(Query)

```ts
id?: string
```

```ts
job?: string
```

```ts
fuzzing_target?: string
```

```ts
engine?: string
```

```ts
page?: integer
```

#### Responses

- 200

`application/json`

```ts
{
  count: integer
  next?: string
  previous?: string
  results: {
    id?: string
    fuzzing_target: string
    job: string
    engine: string
    weight?: number
    last_run: string
  }[]
}
```

---

### [POST]/fuzztargetjob/

#### RequestBody

- application/json

```ts
{
  id?: string
  fuzzing_target: string
  job: string
  engine: string
  weight?: number
  last_run: string
}
```

#### Responses

- 201

`application/json`

```ts
{
  id?: string
  fuzzing_target: string
  job: string
  engine: string
  weight?: number
  last_run: string
}
```

---

### [PATCH]/fuzztargetjob//

#### RequestBody

- application/json

```ts
{
  id?: string
  fuzzing_target: string
  job: string
  engine: string
  weight?: number
  last_run: string
}
```

#### Responses

- 200

`application/json`

```ts
{
  id?: string
  fuzzing_target: string
  job: string
  engine: string
  weight?: number
  last_run: string
}
```

---

### [DELETE]/fuzztargetjob//

#### Responses

- 204

---

### [GET]/job/

#### Parameters(Query)

```ts
id?: string
```

```ts
name?: string
```

```ts
page?: integer
```

#### Responses

- 200

`application/json`

```ts
{
  count: integer
  next?: string
  previous?: string
  results: {
    id?: string
    name: string
    description: string
    project: string
    date: string
    enabled?: boolean
    archived?: boolean
    platform?: enum[Android, Linux, Mac, Windows, NA]
    environment_string?: string
    template?: string
    custom_binary_path?: string
    custom_binary_filename?: string
    custom_binary_revision?: integer
  }[]
}
```

---

### [POST]/job/

#### RequestBody

- application/json

```ts
{
  id?: string
  name: string
  description: string
  project: string
  date: string
  enabled?: boolean
  archived?: boolean
  platform?: enum[Android, Linux, Mac, Windows, NA]
  environment_string?: string
  template?: string
  custom_binary_path?: string
  custom_binary_filename?: string
  custom_binary_revision?: integer
}
```

#### Responses

- 201

`application/json`

```ts
{
  id?: string
  name: string
  description: string
  project: string
  date: string
  enabled?: boolean
  archived?: boolean
  platform?: enum[Android, Linux, Mac, Windows, NA]
  environment_string?: string
  template?: string
  custom_binary_path?: string
  custom_binary_filename?: string
  custom_binary_revision?: integer
}
```

---

### [PATCH]/job//

#### RequestBody

- application/json

```ts
{
  id?: string
  name: string
  description: string
  project: string
  date: string
  enabled?: boolean
  archived?: boolean
  platform?: enum[Android, Linux, Mac, Windows, NA]
  environment_string?: string
  template?: string
  custom_binary_path?: string
  custom_binary_filename?: string
  custom_binary_revision?: integer
}
```

#### Responses

- 200

`application/json`

```ts
{
  id?: string
  name: string
  description: string
  project: string
  date: string
  enabled?: boolean
  archived?: boolean
  platform?: enum[Android, Linux, Mac, Windows, NA]
  environment_string?: string
  template?: string
  custom_binary_path?: string
  custom_binary_filename?: string
  custom_binary_revision?: integer
}
```

---

### [DELETE]/job//

#### Responses

- 204

---

### [GET]/jobtemplate/

#### Parameters(Query)

```ts
id?: string
```

```ts
name?: string
```

#### Responses

- 200

`application/json`

```ts
{
  id?: string
  name: string
  environment_string?: string
}[]
```

---

### [POST]/jobtemplate/

#### RequestBody

- application/json

```ts
{
  id?: string
  name: string
  environment_string?: string
}
```

#### Responses

- 201

`application/json`

```ts
{
  id?: string
  name: string
  environment_string?: string
}
```

---

### [PATCH]/jobtemplate//

#### RequestBody

- application/json

```ts
{
  id?: string
  name: string
  environment_string?: string
}
```

#### Responses

- 200

`application/json`

```ts
{
  id?: string
  name: string
  environment_string?: string
}
```

---

### [DELETE]/jobtemplate//

#### Responses

- 204

---

### [GET]/stadistics/

#### Parameters(Query)

```ts
id?: string
```

```ts
page?: integer
```

#### Responses

- 200

`application/json`

```ts
{
  count: integer
  next?: string
  previous?: string
  results: {
    id?: string
    job_id: string
    iteration: integer
    runtime: integer
    execs_per_sec: integer
    date: string
    last_beat_time: string
    status: string
    task_payload: string
  }[]
}
```

---

### [POST]/stadistics/

#### RequestBody

- application/json

```ts
{
  id?: string
  job_id: string
  iteration: integer
  runtime: integer
  execs_per_sec: integer
  date: string
  last_beat_time: string
  status: string
  task_payload: string
}
```

#### Responses

- 201

`application/json`

```ts
{
  id?: string
  job_id: string
  iteration: integer
  runtime: integer
  execs_per_sec: integer
  date: string
  last_beat_time: string
  status: string
  task_payload: string
}
```

---

### [PATCH]/stadistics//

#### RequestBody

- application/json

```ts
{
  id?: string
  job_id: string
  iteration: integer
  runtime: integer
  execs_per_sec: integer
  date: string
  last_beat_time: string
  status: string
  task_payload: string
}
```

#### Responses

- 200

`application/json`

```ts
{
  id?: string
  job_id: string
  iteration: integer
  runtime: integer
  execs_per_sec: integer
  date: string
  last_beat_time: string
  status: string
  task_payload: string
}
```

---

### [DELETE]/stadistics//

#### Responses

- 204

---

### [GET]/task/

#### Responses

- 200

---

### [POST]/task/

#### Responses

- 201

---

### [GET]/testcase/

#### Parameters(Query)

```ts
id?: string
```

```ts
job_id?: string
```

```ts
job_id__project?: string
```

```ts
crash_testcase__crash_type?: string
```

```ts
crash_testcase__crash_state?: string
```

```ts
crash_testcase__security_flag?: string
```

```ts
page?: integer
```

#### Responses

- 200

`application/json`

```ts
{
  count: integer
  next?: string
  previous?: string
  results: {
    id?: string
    bug_information?: string
    test_case: string
    fixed?: string
    one_time_crasher_flag?: boolean
    comments?: string
    absolute_path?: string
    queue?: string
    archived?: boolean
    timestamp: string
    status?: enum[pending, processed, unreproducible, done]
    triaged?: boolean
    has_bug_flag?: boolean
    open?: boolean
    testcase_path?: string
    additional_metadata?: string
    fuzzed_keys?: string
    minimized_keys?: string
    minidump_keys?: string
    minimized_arguments?: string
    disable_ubsan?: boolean
    regression?: string
    timeout_multiplier?: number
    archive_state?: integer
    redzone?: integer
    job_id: string
    fuzzer_id: string
  }[]
}
```

---

### [POST]/testcase/

#### RequestBody

- application/json

```ts
{
  id?: string
  bug_information?: string
  test_case: string
  fixed?: string
  one_time_crasher_flag?: boolean
  comments?: string
  absolute_path?: string
  queue?: string
  archived?: boolean
  timestamp: string
  status?: enum[pending, processed, unreproducible, done]
  triaged?: boolean
  has_bug_flag?: boolean
  open?: boolean
  testcase_path?: string
  additional_metadata?: string
  fuzzed_keys?: string
  minimized_keys?: string
  minidump_keys?: string
  minimized_arguments?: string
  disable_ubsan?: boolean
  regression?: string
  timeout_multiplier?: number
  archive_state?: integer
  redzone?: integer
  job_id: string
  fuzzer_id: string
}
```

#### Responses

- 201

`application/json`

```ts
{
  id?: string
  bug_information?: string
  test_case: string
  fixed?: string
  one_time_crasher_flag?: boolean
  comments?: string
  absolute_path?: string
  queue?: string
  archived?: boolean
  timestamp: string
  status?: enum[pending, processed, unreproducible, done]
  triaged?: boolean
  has_bug_flag?: boolean
  open?: boolean
  testcase_path?: string
  additional_metadata?: string
  fuzzed_keys?: string
  minimized_keys?: string
  minidump_keys?: string
  minimized_arguments?: string
  disable_ubsan?: boolean
  regression?: string
  timeout_multiplier?: number
  archive_state?: integer
  redzone?: integer
  job_id: string
  fuzzer_id: string
}
```

---

### [PATCH]/testcase//

#### RequestBody

- application/json

```ts
{
  id?: string
  bug_information?: string
  test_case: string
  fixed?: string
  one_time_crasher_flag?: boolean
  comments?: string
  absolute_path?: string
  queue?: string
  archived?: boolean
  timestamp: string
  status?: enum[pending, processed, unreproducible, done]
  triaged?: boolean
  has_bug_flag?: boolean
  open?: boolean
  testcase_path?: string
  additional_metadata?: string
  fuzzed_keys?: string
  minimized_keys?: string
  minidump_keys?: string
  minimized_arguments?: string
  disable_ubsan?: boolean
  regression?: string
  timeout_multiplier?: number
  archive_state?: integer
  redzone?: integer
  job_id: string
  fuzzer_id: string
}
```

#### Responses

- 200

`application/json`

```ts
{
  id?: string
  bug_information?: string
  test_case: string
  fixed?: string
  one_time_crasher_flag?: boolean
  comments?: string
  absolute_path?: string
  queue?: string
  archived?: boolean
  timestamp: string
  status?: enum[pending, processed, unreproducible, done]
  triaged?: boolean
  has_bug_flag?: boolean
  open?: boolean
  testcase_path?: string
  additional_metadata?: string
  fuzzed_keys?: string
  minimized_keys?: string
  minidump_keys?: string
  minimized_arguments?: string
  disable_ubsan?: boolean
  regression?: string
  timeout_multiplier?: number
  archive_state?: integer
  redzone?: integer
  job_id: string
  fuzzer_id: string
}
```

---

### [DELETE]/testcase//

#### Responses

- 204

---

### [GET]/testcasevariant/

#### Parameters(Query)

```ts
id?: string
```

```ts
testcase_id?: string
```

```ts
job_id?: string
```

```ts
page?: integer
```

#### Responses

- 200

`application/json`

```ts
{
  count: integer
  next?: string
  previous?: string
  results: {
    id?: string
    status?: enum[0, 1, 2, 3]
    testcase_id: string
    job_id: string
    revision?: integer
    crash_type?: string
    crash_state?: string
    security_flag?: boolean
    is_similar?: boolean
    reproducer_key?: string
    platform?: enum[Android, Linux, Mac, Windows, NA]
  }[]
}
```

---

### [POST]/testcasevariant/

#### RequestBody

- application/json

```ts
{
  id?: string
  status?: enum[0, 1, 2, 3]
  testcase_id: string
  job_id: string
  revision?: integer
  crash_type?: string
  crash_state?: string
  security_flag?: boolean
  is_similar?: boolean
  reproducer_key?: string
  platform?: enum[Android, Linux, Mac, Windows, NA]
}
```

#### Responses

- 201

`application/json`

```ts
{
  id?: string
  status?: enum[0, 1, 2, 3]
  testcase_id: string
  job_id: string
  revision?: integer
  crash_type?: string
  crash_state?: string
  security_flag?: boolean
  is_similar?: boolean
  reproducer_key?: string
  platform?: enum[Android, Linux, Mac, Windows, NA]
}
```

---

### [PATCH]/testcasevariant//

#### RequestBody

- application/json

```ts
{
  id?: string
  status?: enum[0, 1, 2, 3]
  testcase_id: string
  job_id: string
  revision?: integer
  crash_type?: string
  crash_state?: string
  security_flag?: boolean
  is_similar?: boolean
  reproducer_key?: string
  platform?: enum[Android, Linux, Mac, Windows, NA]
}
```

#### Responses

- 200

`application/json`

```ts
{
  id?: string
  status?: enum[0, 1, 2, 3]
  testcase_id: string
  job_id: string
  revision?: integer
  crash_type?: string
  crash_state?: string
  security_flag?: boolean
  is_similar?: boolean
  reproducer_key?: string
  platform?: enum[Android, Linux, Mac, Windows, NA]
}
```

---

### [DELETE]/testcasevariant//

#### Responses

- 204

---

### [POST]/token/

- Description
  Takes a set of user credentials and returns an access and refresh JSON web
  token pair to prove the authentication of those credentials.

#### RequestBody

- application/json

```ts
{
  username: string
  password: string
}
```

#### Responses

- 201

`application/json`

```ts
{
  username: string
  password: string
}
```

---

### [POST]/token/refresh/

- Description
  Takes a refresh type JSON web token and returns an access type JSON web
  token if the refresh token is valid.

#### RequestBody

- application/json

```ts
{
  refresh: string
  access?: string
}
```

#### Responses

- 201

`application/json`

```ts
{
  refresh: string
  access?: string
}
```

---

### [GET]/trial/

#### Parameters(Query)

```ts
id?: string
```

```ts
app_name?: string
```

```ts
page?: integer
```

#### Responses

- 200

`application/json`

```ts
{
  count: integer
  next?: string
  previous?: string
  results: {
    id?: string
    app_name: string
    probability?: number
    app_args?: string
  }[]
}
```

---

### [POST]/trial/

#### RequestBody

- application/json

```ts
{
  id?: string
  app_name: string
  probability?: number
  app_args?: string
}
```

#### Responses

- 201

`application/json`

```ts
{
  id?: string
  app_name: string
  probability?: number
  app_args?: string
}
```

---

### [PATCH]/trial//

#### RequestBody

- application/json

```ts
{
  id?: string
  app_name: string
  probability?: number
  app_args?: string
}
```

#### Responses

- 200

`application/json`

```ts
{
  id?: string
  app_name: string
  probability?: number
  app_args?: string
}
```

---

### [DELETE]/trial//

#### Responses

- 204

## References

### #/components/requestBodies/FuzzTarget

- application/json

```ts
{
  id?: string
  fuzzer_engine: string
  project: string
  binary: string
}
```

### #/components/requestBodies/BuildMetadata

- application/json

```ts
{
  id?: string
  job?: string
  revision?: integer
  bad_build?: boolean
  console_output?: string
  bot_name: string
  symbols?: string
  timestamp: string
}
```

### #/components/requestBodies/JobTemplate

- application/json

```ts
{
  id?: string
  name: string
  environment_string?: string
}
```

### #/components/requestBodies/Bot

- application/json

```ts
{
  id?: string
  name: string
  last_beat_time?: string
  task_payload?: string
  task_end_time?: string
  task_status?: enum[started, in-progress, finished, errored out, NA]
  platform?: enum[Android, Linux, Mac, Windows, NA]
  blobstore_log_path?: string
  bot_logs?: string
}
```

### #/components/requestBodies/TestCase

- application/json

```ts
{
  id?: string
  bug_information?: string
  test_case: string
  fixed?: string
  one_time_crasher_flag?: boolean
  comments?: string
  absolute_path?: string
  queue?: string
  archived?: boolean
  timestamp: string
  status?: enum[pending, processed, unreproducible, done]
  triaged?: boolean
  has_bug_flag?: boolean
  open?: boolean
  testcase_path?: string
  additional_metadata?: string
  fuzzed_keys?: string
  minimized_keys?: string
  minidump_keys?: string
  minimized_arguments?: string
  disable_ubsan?: boolean
  regression?: string
  timeout_multiplier?: number
  archive_state?: integer
  redzone?: integer
  job_id: string
  fuzzer_id: string
}
```

### #/components/requestBodies/Coverage

- application/json

```ts
{
  id?: string
  date: string
  fuzzer: string
  functions_covered: integer
  functions_total: integer
  edges_covered: integer
  edges_total: integer
  corpus_size_units: integer
  corpus_size_bytes: integer
  corpus_location: string
  corpus_backup_location: string
  quarantine_size_units: integer
  quarantine_size_bytes: integer
  quarantine_location: string
  html_report_url?: string
  testcase: string
}
```

### #/components/requestBodies/TestCaseVariant

- application/json

```ts
{
  id?: string
  status?: enum[0, 1, 2, 3]
  testcase_id: string
  job_id: string
  revision?: integer
  crash_type?: string
  crash_state?: string
  security_flag?: boolean
  is_similar?: boolean
  reproducer_key?: string
  platform?: enum[Android, Linux, Mac, Windows, NA]
}
```

### #/components/requestBodies/FuzzTargetJob

- application/json

```ts
{
  id?: string
  fuzzing_target: string
  job: string
  engine: string
  weight?: number
  last_run: string
}
```

### #/components/requestBodies/TokenRefresh

- application/json

```ts
{
  refresh: string
  access?: string
}
```

### #/components/requestBodies/Crash

- application/json

```ts
{
  id?: string
  testcase_id: string
  crash_signal: integer
  exploitability?: string
  crash_time: integer
  crash_hash: string
  verified?: boolean
  additional?: string
  iteration: integer
  crash_type: string
  crash_address?: string
  crash_state: string
  crash_stacktrace: string
  regression?: string
  security_severity?: integer
  absolute_path: string
  security_flag: boolean
  reproducible_flag?: boolean
  return_code: string
  gestures: {
  }
  resource_list: {
  }
  fuzzing_strategy: {
  }
  should_be_ignored?: boolean
  application_command_line?: string
  unsymbolized_crash_stacktrace: string
  crash_frame: {
  }
  crash_info?: string
  crash_revision?: integer
}
```

### #/components/requestBodies/DataBundle

- application/json

```ts
{
  id?: string
  name: string
  bucket_name: string
  source?: string
  is_local?: boolean
  timestamp: string
  sync_to_worker?: boolean
}
```

### #/components/requestBodies/Fuzzer

- application/json

```ts
{
  id?: string
  timestamp?: string
  name: string
  filename?: string
  file_size?: integer
  // Content of the file base64 encoded
  fuzzer_zip?: string
  blobstore_path?: string
  executable_path?: string
  revision?: number
  timeout?: integer
  supported_platforms?: enum[Android, Linux, Mac, Windows, NA]
  launcher_script?: string
  result?: string
  result_timestamp?: string
  console_output?: string
  return_code?: integer
  sample_testcase?: string
  max_testcases?: integer
  untrusted_content?: boolean
  additional_environment_string?: string
  stats_columns: {
  }
  stats_column_descriptions: {
  }
  builtin?: boolean
  differential?: boolean
  has_large_testcases?: boolean
  data_bundle_name?: string
}
```

### #/components/requestBodies/Job

- application/json

```ts
{
  id?: string
  name: string
  description: string
  project: string
  date: string
  enabled?: boolean
  archived?: boolean
  platform?: enum[Android, Linux, Mac, Windows, NA]
  environment_string?: string
  template?: string
  custom_binary_path?: string
  custom_binary_filename?: string
  custom_binary_revision?: integer
}
```

### #/components/requestBodies/Statistic

- application/json

```ts
{
  id?: string
  job_id: string
  iteration: integer
  runtime: integer
  execs_per_sec: integer
  date: string
  last_beat_time: string
  status: string
  task_payload: string
}
```

### #/components/requestBodies/Trial

- application/json

```ts
{
  id?: string
  app_name: string
  probability?: number
  app_args?: string
}
```

### #/components/securitySchemes/Basic

```ts
{
  "type": "http",
  "scheme": "basic"
}
```

### #/components/schemas/AuthToken

```ts
{
  username: string
  password: string
  token?: string
}
```

### #/components/schemas/Login

```ts
{
  username: string
  password: string
}
```

### #/components/schemas/TokenRefresh

```ts
{
  refresh: string
  access?: string
}
```

### #/components/schemas/Register

```ts
{
  id?: integer
  // Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.
  username: string
  email: string
  password: string
  // Designates whether this user should be treated as active. Unselect this instead of deleting accounts.
  is_active?: boolean
}
```

### #/components/schemas/Bot

```ts
{
  id?: string
  name: string
  last_beat_time?: string
  task_payload?: string
  task_end_time?: string
  task_status?: enum[started, in-progress, finished, errored out, NA]
  platform?: enum[Android, Linux, Mac, Windows, NA]
  blobstore_log_path?: string
  bot_logs?: string
}
```

### #/components/schemas/BuildMetadata

```ts
{
  id?: string
  job?: string
  revision?: integer
  bad_build?: boolean
  console_output?: string
  bot_name: string
  symbols?: string
  timestamp: string
}
```

### #/components/schemas/Coverage

```ts
{
  id?: string
  date: string
  fuzzer: string
  functions_covered: integer
  functions_total: integer
  edges_covered: integer
  edges_total: integer
  corpus_size_units: integer
  corpus_size_bytes: integer
  corpus_location: string
  corpus_backup_location: string
  quarantine_size_units: integer
  quarantine_size_bytes: integer
  quarantine_location: string
  html_report_url?: string
  testcase: string
}
```

### #/components/schemas/Crash

```ts
{
  id?: string
  testcase_id: string
  crash_signal: integer
  exploitability?: string
  crash_time: integer
  crash_hash: string
  verified?: boolean
  additional?: string
  iteration: integer
  crash_type: string
  crash_address?: string
  crash_state: string
  crash_stacktrace: string
  regression?: string
  security_severity?: integer
  absolute_path: string
  security_flag: boolean
  reproducible_flag?: boolean
  return_code: string
  gestures: {
  }
  resource_list: {
  }
  fuzzing_strategy: {
  }
  should_be_ignored?: boolean
  application_command_line?: string
  unsymbolized_crash_stacktrace: string
  crash_frame: {
  }
  crash_info?: string
  crash_revision?: integer
}
```

### #/components/schemas/DataBundle

```ts
{
  id?: string
  name: string
  bucket_name: string
  source?: string
  is_local?: boolean
  timestamp: string
  sync_to_worker?: boolean
}
```

### #/components/schemas/Fuzzer

```ts
{
  id?: string
  timestamp?: string
  name: string
  filename?: string
  file_size?: integer
  // Content of the file base64 encoded
  fuzzer_zip?: string
  blobstore_path?: string
  executable_path?: string
  revision?: number
  timeout?: integer
  supported_platforms?: enum[Android, Linux, Mac, Windows, NA]
  launcher_script?: string
  result?: string
  result_timestamp?: string
  console_output?: string
  return_code?: integer
  sample_testcase?: string
  max_testcases?: integer
  untrusted_content?: boolean
  additional_environment_string?: string
  stats_columns: {
  }
  stats_column_descriptions: {
  }
  builtin?: boolean
  differential?: boolean
  has_large_testcases?: boolean
  data_bundle_name?: string
}
```

### #/components/schemas/FuzzTarget

```ts
{
  id?: string
  fuzzer_engine: string
  project: string
  binary: string
}
```

### #/components/schemas/FuzzTargetJob

```ts
{
  id?: string
  fuzzing_target: string
  job: string
  engine: string
  weight?: number
  last_run: string
}
```

### #/components/schemas/Job

```ts
{
  id?: string
  name: string
  description: string
  project: string
  date: string
  enabled?: boolean
  archived?: boolean
  platform?: enum[Android, Linux, Mac, Windows, NA]
  environment_string?: string
  template?: string
  custom_binary_path?: string
  custom_binary_filename?: string
  custom_binary_revision?: integer
}
```

### #/components/schemas/JobTemplate

```ts
{
  id?: string
  name: string
  environment_string?: string
}
```

### #/components/schemas/Statistic

```ts
{
  id?: string
  job_id: string
  iteration: integer
  runtime: integer
  execs_per_sec: integer
  date: string
  last_beat_time: string
  status: string
  task_payload: string
}
```

### #/components/schemas/TestCase

```ts
{
  id?: string
  bug_information?: string
  test_case: string
  fixed?: string
  one_time_crasher_flag?: boolean
  comments?: string
  absolute_path?: string
  queue?: string
  archived?: boolean
  timestamp: string
  status?: enum[pending, processed, unreproducible, done]
  triaged?: boolean
  has_bug_flag?: boolean
  open?: boolean
  testcase_path?: string
  additional_metadata?: string
  fuzzed_keys?: string
  minimized_keys?: string
  minidump_keys?: string
  minimized_arguments?: string
  disable_ubsan?: boolean
  regression?: string
  timeout_multiplier?: number
  archive_state?: integer
  redzone?: integer
  job_id: string
  fuzzer_id: string
}
```

### #/components/schemas/TestCaseVariant

```ts
{
  id?: string
  status?: enum[0, 1, 2, 3]
  testcase_id: string
  job_id: string
  revision?: integer
  crash_type?: string
  crash_state?: string
  security_flag?: boolean
  is_similar?: boolean
  reproducer_key?: string
  platform?: enum[Android, Linux, Mac, Windows, NA]
}
```

### #/components/schemas/TokenObtainPair

```ts
{
  username: string
  password: string
}
```

### #/components/schemas/Trial

```ts
{
  id?: string
  app_name: string
  probability?: number
  app_args?: string
}
```
