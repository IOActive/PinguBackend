# Snippets API

> Version v1

This document provides an overview of the available API endpoints in the PinguCrew backend.

## Path Table

| Method | Path                                        | Description                      |
| ------ | ------------------------------------------- | -------------------------------- |
| POST   | [/api-token-auth/](#postapi-token-auth)        | Obtain an authentication token.  |
| POST   | [/auth/login/](#postauthlogin)                 | Login to the system.             |
| POST   | [/auth/refresh/](#postauthrefresh)             | Refresh an authentication token. |
| POST   | [/auth/register/](#postauthregister)           | Register a new user.             |
| GET    | [/bot/](#getbot)                               | List all bots.                   |
| POST   | [/bot/](#postbot)                              | Create a new bot.                |
| PATCH  | [/bot/{id}/](#patchbotid)                      | Update a bot.                    |
| DELETE | [/bot/{id}/](#deletebotid)                     | Delete a bot.                    |
| GET    | [/buildmetadata/](#getbuildmetadata)           | List build metadata.             |
| POST   | [/buildmetadata/](#postbuildmetadata)          | Create build metadata.           |
| PATCH  | [/buildmetadata/{id}/](#patchbuildmetadataid)  | Update build metadata.           |
| DELETE | [/buildmetadata/{id}/](#deletebuildmetadataid) | Delete build metadata.           |
| GET    | [/coverage/](#getcoverage)                     | List coverage data.              |
| POST   | [/coverage/](#postcoverage)                    | Upload coverage data.            |
| PATCH  | [/coverage/{id}/](#patchcoverageid)            | Update coverage data.            |
| DELETE | [/coverage/{id}/](#deletecoverageid)           | Delete coverage data.            |
| GET    | [/crash/](#getcrash)                           | List crash data.                 |
| POST   | [/crash/](#postcrash)                          | Create crash data.               |
| PATCH  | [/crash/{id}/](#patchcrashid)                  | Update crash data.               |
| DELETE | [/crash/{id}/](#deletecrashid)                 | Delete crash data.               |
| GET    | [/databundle/](#getdatabundle)                 | List data bundles.               |
| POST   | [/databundle/](#postdatabundle)                | Create a data bundle.            |
| PATCH  | [/databundle/{id}/](#patchdatabundleid)        | Update a data bundle.            |
| DELETE | [/databundle/{id}/](#deletedatabundleid)       | Delete a data bundle.            |
| GET    | [/fuzzer/](#getfuzzer)                         | List fuzzers.                    |
| POST   | [/fuzzer/](#postfuzzer)                        | Create a fuzzer.                 |
| PATCH  | [/fuzzer/{id}/](#patchfuzzerid)                | Update a fuzzer.                 |
| DELETE | [/fuzzer/{id}/](#deletefuzzerid)               | Delete a fuzzer.                 |
| GET    | [/fuzztarget/](#getfuzztarget)                 | List fuzz targets.               |
| POST   | [/fuzztarget/](#postfuzztarget)                | Create a fuzz target.            |
| PATCH  | [/fuzztarget/{id}/](#patchfuzztargetid)        | Update a fuzz target.            |
| DELETE | [/fuzztarget/{id}/](#deletefuzztargetid)       | Delete a fuzz target.            |
| GET    | [/job/](#getjob)                               | List jobs.                       |
| POST   | [/job/](#postjob)                              | Create a job.                    |
| PATCH  | [/job/{id}/](#patchjobid)                      | Update a job.                    |
| DELETE | [/job/{id}/](#deletejobid)                     | Delete a job.                    |
| GET    | [/stadistics/](#getstadistics)                 | List statistics.                 |
| POST   | [/stadistics/](#poststadistics)                | Create statistics.               |
| PATCH  | [/stadistics/{id}/](#patchstadisticsid)        | Update statistics.               |
| DELETE | [/stadistics/{id}/](#deletestadisticsid)       | Delete statistics.               |

# Notes

- For detailed API schemas, refer to the [Swagger JSON](swagger.json) or navigate to the [Backend Swagger](http://localhost:8086/api/swagger/).
